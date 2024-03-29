from codenames.data.codenames_pb2 import ActionOutcome
from codenames.data.codenames_pb2 import Role
from codenames.data.codenames_pb2 import SharedAction
from codenames.data.codenames_pb2 import SharedClue
from codenames.data.types import Codename
from codenames.data.types import EndTurn
from codenames.data.types import NullTeam
from codenames.data.types import Team
from codenames.game.game_state import GameState
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

    def play(self) -> None:
        while not self._game_finished():
            self._logger.log_active_player(
                self.game_state.active_team, self.game_state.active_role
            )
            if self.game_state.active_role == Role.CLUE_GIVER:
                self._execute_clue_phase()
            elif self.game_state.active_role == Role.GUESSER:
                self._execute_action_phase()
            else:
                self._logger.log_invalid_role(self.game_state.active_role)
                raise TypeError

    def _set_up_players(self):
        common_information = self.game_state.get_common_information()
        secret_information = self.game_state.get_secret_information()
        self._logger.log_secret_information(secret_information)
        for team, team_players in self._players.items():
            team_players.clue_giver.set_up(team, common_information)
            team_players.guesser.set_up(team, common_information)
            team_players.clue_giver.reaveal_secret_information(
                secret_information
            )

    def _game_finished(self) -> bool:
        if self.game_state.teams_remaining() == 1:
            return True
        if self.game_state.active_team == NullTeam:
            return True
        return False

    def _execute_clue_phase(self) -> None:
        clue_giver = self._players[self.game_state.active_team].clue_giver
        clue = clue_giver.give_clue()
        self._logger.log_clue(clue)
        self.game_state.resolve_clue(clue)
        shared_clue = SharedClue(team=self.game_state.active_team, clue=clue)
        self._logger.log_shared_clue(shared_clue)
        for team_players in self._players.values():
            team_players.clue_giver.reveal_clue(shared_clue)
            team_players.guesser.reveal_clue(shared_clue)

    def _execute_action_phase(self) -> None:
        guesser = self._players[self.game_state.active_team].guesser
        action = guesser.give_action()
        self._logger.log_action(action)
        self.game_state.resolve_action(action)
        if action.guess == EndTurn:
            action_outcome = ActionOutcome(identity=NullTeam)
        else:
            identity = self.game_state.codename_identity(Codename(action.guess))
            action_outcome = ActionOutcome(identity=identity)
        shared_action = SharedAction(
            team=self.game_state.active_team,
            action=action,
            action_outcome=action_outcome,
        )
        self._logger.log_shared_action(shared_action)
        for team_players in self._players.values():
            team_players.clue_giver.reveal_action(shared_action)
            team_players.guesser.reveal_action(shared_action)
