from collections import defaultdict
from typing import Optional

from codenames.data.codenames_pb2 import Action
from codenames.data.codenames_pb2 import Clue
from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import Role
from codenames.data.codenames_pb2 import SecretInformation
from codenames.data.types import Codename
from codenames.data.types import CodenameIdentities
from codenames.data.types import EndTurn
from codenames.data.types import FatalTeam
from codenames.data.types import IdentityCodenames
from codenames.data.types import NonPlayerTeams
from codenames.data.types import Quantity
from codenames.data.types import Team
from codenames.data.types import TeamOutcomes
from codenames.data.types import UnknownTeam
from codenames.data.types import Unlimited
import codenames.data.utils as du
from codenames.game.player_team_list import PlayerTeamList


class GameState:

    def __init__(
        self, codename_identities: CodenameIdentities,
        unknown_agents: IdentityCodenames, player_teams: PlayerTeamList,
        team_outcomes: TeamOutcomes, active_role: int,
        guesses_remaining: Quantity
    ) -> None:
        self._codename_identities = codename_identities
        self._unknown_agents = unknown_agents
        self._player_teams = player_teams
        self._team_outcomes = team_outcomes
        self._active_role = active_role
        self._guesses_remaining = guesses_remaining

    @classmethod
    def from_secret_information(
        cls,
        secret_information: SecretInformation,
        ordered_teams: Optional[list[Team]] = None
    ) -> 'GameState':
        if ordered_teams is None:
            ordered_teams = cls._get_ordered_teams(secret_information)
        codename_identities = cls._get_codename_identities(secret_information)
        unknown_agents = cls._get_unknown_agents(secret_information)
        player_teams = PlayerTeamList(ordered_teams)
        team_outcomes = cls._get_team_outcomes(ordered_teams, unknown_agents)
        active_role = Role.CLUE_GIVER
        guesses_remaining = Quantity(0)
        return GameState(
            codename_identities,
            unknown_agents,
            player_teams,
            team_outcomes,
            active_role,
            guesses_remaining,
        )

    @classmethod
    def _get_ordered_teams(cls,
                           secret_information: SecretInformation) -> list[Team]:
        all_teams = set(secret_information.agent_sets.keys())
        player_teams = all_teams - NonPlayerTeams
        return sorted(list(map(Team, player_teams)))

    @classmethod
    def _get_codename_identities(
        cls, secret_information: SecretInformation
    ) -> CodenameIdentities:
        return CodenameIdentities({
            Codename(codename): Team(team)
            for team, agent_set in secret_information.agent_sets.items()
            for codename in agent_set.codenames
        })

    @classmethod
    def _get_unknown_agents(
        cls, secret_information: SecretInformation
    ) -> IdentityCodenames:
        return IdentityCodenames({
            Team(team): set(map(Codename, agent_set.codenames))
            for team, agent_set in secret_information.agent_sets.items()
        })

    @classmethod
    def _get_team_outcomes(
        cls, player_teams: list[Team], unknown_agents: IdentityCodenames
    ) -> TeamOutcomes:
        found_agents = [
            team for team in player_teams if not unknown_agents[team]
        ]
        return TeamOutcomes(found_agents=found_agents)

    @property
    def active_team(self):
        return self._player_teams.active_team

    @property
    def active_role(self):
        return self._active_role

    def teams_remaining(self) -> int:
        return len(self._player_teams)

    def codename_identity(self, codename: Codename):
        return self._codename_identities[codename]

    def get_common_information(self) -> CommonInformation:
        common_information = CommonInformation()
        for team, count in self._get_identity_counts().items():
            common_information.identity_counts[team] = count
        for team, codenames in self._get_agent_sets().items():
            common_information.agent_sets[team].codenames.extend(codenames)
        # turn history cannot be completely inferred from game state
        return common_information

    def get_secret_information(self) -> SecretInformation:
        secret_information = SecretInformation()
        identity_codenames = du.codename_identities_to_identity_codenames(
            self._codename_identities
        )
        for team, codenames in identity_codenames.items():
            secret_information.agent_sets[team].codenames.extend(codenames)
        return secret_information

    def update_state(self, common_information: CommonInformation) -> None:
        for turn in common_information.turn_history:
            self.resolve_clue(turn.clue.clue)
            for action in turn.actions:
                self.resolve_action(action.action)

    def resolve_clue(self, clue: Clue) -> None:
        if not self._validate_clue(clue):
            raise ValueError
        self._guesses_remaining = Quantity(clue.quantity)
        self._active_role = Role.GUESSER

    def resolve_action(self, action: Action) -> None:
        if not self._validate_action(action):
            raise ValueError
        if action.guess == EndTurn:
            self._end_turn()
        else:
            guess = Codename(action.guess)
            self._resolve_guess(guess)

    def _get_identity_counts(self) -> dict[Team, int]:
        return {
            team: len(codenames)
            for team, codenames in self._unknown_agents.items()
        }

    def _get_agent_sets(self) -> dict[Team, list[Codename]]:
        agent_sets: dict[Team, list[Codename]] = defaultdict(list)
        for codename, identity in self._codename_identities.items():
            if codename in self._unknown_agents[identity]:
                agent_sets[UnknownTeam].append(codename)
            else:
                agent_sets[identity].append(codename)
        return agent_sets

    def _resolve_guess(self, guess: Codename) -> None:
        identity = self._codename_identities[guess]
        self._unknown_agents[identity].remove(guess)
        if identity in NonPlayerTeams:
            self._resolve_non_player_team_guess(identity)
        else:
            self._resolve_player_team_guess(identity)

    def _resolve_non_player_team_guess(self, identity: Team) -> None:
        if identity == FatalTeam:
            self._resolve_fatal()
        self._end_turn()

    def _resolve_player_team_guess(self, identity: Team) -> None:
        if not self._unknown_agents[identity]:
            self._resolve_found_agents(identity)
        if identity == self._player_teams.active_team:
            self._resolve_successful_guess()
        else:
            self._end_turn()

    def _resolve_found_agents(self, team: Team) -> None:
        del self._player_teams[team]
        self._team_outcomes.found_agents.append(team)

    def _resolve_fatal(self) -> None:
        team = self._player_teams.active_team
        del self._player_teams[team]
        self._team_outcomes.found_fatal.append(team)

    def _resolve_successful_guess(self) -> None:
        if self._guesses_remaining != Unlimited:
            self._guesses_remaining = Quantity(self._guesses_remaining - 1)
        if self._guesses_remaining == Quantity(0):
            self._end_turn()

    def _end_turn(self) -> None:
        _ = next(self._player_teams)
        self._active_role = Role.CLUE_GIVER
        self._guesses_remaining = Quantity(0)

    def _validate_clue(self, clue: Clue) -> bool:
        if clue.word in self._codename_identities:
            return False
        if not (clue.quantity > 0 or clue.quantity == Unlimited):
            return False
        return True

    def _validate_action(self, action: Action) -> bool:
        if not (action.guess in self._codename_identities
                or action.guess == EndTurn):
            return False
        return True
