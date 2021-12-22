from codenames.data.codenames_pb2 import (
    ActionOutcome, Role, SharedAction, SharedClue
)
from codenames.data.types import EndTurn, NullTeam, Team, UnknownTeam
from codenames.game.game_state_evolution import resolve_action, resolve_clue
from codenames.game.game_state import GameState
from codenames.players.team_players import TeamPlayers


class Game:

    def __init__(
        self, players: dict[Team, TeamPlayers], game_state: GameState
    ) -> None:
        self._players = players
        self._game_state = game_state

    @property
    def game_state(self) -> GameState:
        return self._game_state

    @property
    def _active_team(self) -> Team:
        return self.game_state.teams.active_team

    def play(self) -> None:
        while self._game_unfinished():
            if self.game_state.active_role == Role.CODEMASTER:
                self._execute_clue_phase()
            elif self.game_state.active_role == Role.INTERPRETER:
                self._execute_action_phase()
            else:
                raise TypeError

    def _game_unfinished(self) -> bool:
        return self._active_team != NullTeam

    def _execute_clue_phase(self) -> None:
        clue = self._players[self._active_team].codemaster.give_clue()
        resolve_clue(self.game_state, clue)
        shared_clue = SharedClue(team=self._active_team, clue=clue)
        for team_players in self._players.values():
            team_players.codemaster.reveal_clue(shared_clue)
            team_players.interpreter.reveal_clue(shared_clue)

    def _execute_action_phase(self) -> None:
        action = self._players[self._active_team].interpreter.give_action()
        resolve_action(self.game_state, action)
        if action.guess == EndTurn:
            action_outcome = ActionOutcome(identity=NullTeam)
        else:
            action_outcome = ActionOutcome(
                identity=self.game_state.codename_identities
                .get(action.guess, UnknownTeam)
            )
        shared_action = SharedAction(
            team=self._active_team,
            action=action,
            action_outcome=action_outcome,
        )
        for team_players in self._players.values():
            team_players.codemaster.reveal_action(shared_action)
            team_players.interpreter.reveal_action(shared_action)
