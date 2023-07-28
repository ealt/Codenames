from codenames.data.codenames_pb2 import ActionOutcome
from codenames.data.codenames_pb2 import Role
from codenames.data.codenames_pb2 import SharedAction
from codenames.data.codenames_pb2 import SharedClue
from codenames.data.types import Codename
from codenames.data.types import EndTurn
from codenames.data.types import NullTeam
from codenames.data.types import Team
from codenames.game.game_state import GameState
import codenames.game.game_state_evolution as game_state_evolution
import codenames.game.utils as gu
from codenames.logging.game_logger import GameLogger
from codenames.players.team_players import TeamPlayers


class Game:

    def __init__(
        self, players: dict[Team, TeamPlayers], game_state: GameState,
        logger: GameLogger
    ) -> None:
        self._logger = logger
        self._players = players
        self._logger.log_players(players)
        self._game_state = game_state
        self._set_up_players()

    @property
    def game_state(self) -> GameState:
        return self._game_state

    @property
    def _active_team(self) -> Team:
        return self.game_state.teams.active_team

    def play(self) -> None:
        while not self._game_finished():
            self._logger.log_active_player(
                self.game_state.teams.active_team, self.game_state.active_role
            )
            if self.game_state.active_role == Role.CODEMASTER:
                self._execute_clue_phase()
            elif self.game_state.active_role == Role.INTERPRETER:
                self._execute_action_phase()
            else:
                self._logger.log_invalid_role(self.game_state.active_role)
                raise TypeError

    def _set_up_players(self):
        information = gu.get_information(self.game_state)
        self._logger.log_secret_information(information.secret)
        for team, team_players in self._players.items():
            team_players.codemaster.set_up(team, information.common)
            team_players.interpreter.set_up(team, information.common)
            team_players.codemaster.reaveal_secret_information(
                information.secret
            )

    def _game_finished(self) -> bool:
        if len(self.game_state.teams) == 1:
            return True
        if self._active_team == NullTeam:
            return True
        return False

    def _execute_clue_phase(self) -> None:
        clue = self._players[self._active_team].codemaster.give_clue()
        self._logger.log_clue(clue)
        game_state_evolution.resolve_clue(self.game_state, clue)
        shared_clue = SharedClue(team=self._active_team, clue=clue)
        self._logger.log_shared_clue(shared_clue)
        for team_players in self._players.values():
            team_players.codemaster.reveal_clue(shared_clue)
            team_players.interpreter.reveal_clue(shared_clue)

    def _execute_action_phase(self) -> None:
        action = self._players[self._active_team].interpreter.give_action()
        self._logger.log_action(action)
        game_state_evolution.resolve_action(self.game_state, action)
        if action.guess == EndTurn:
            action_outcome = ActionOutcome(identity=NullTeam)
        else:
            identity = self.game_state.codename_identities[Codename(
                action.guess
            )]
            action_outcome = ActionOutcome(identity=identity)
        shared_action = SharedAction(
            team=self._active_team,
            action=action,
            action_outcome=action_outcome,
        )
        self._logger.log_shared_action(shared_action)
        for team_players in self._players.values():
            team_players.codemaster.reveal_action(shared_action)
            team_players.interpreter.reveal_action(shared_action)
