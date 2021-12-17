from codenames.data.codenames_pb2 import Action, Clue, Role
from codenames.data.types import EndTurn, Quantity, Team
from codenames.game.game_state import GameState


def resolve_clue(game_state: GameState, clue: Clue) -> None:
    game_state.guesses_remaining = Quantity(clue.quantity)
    game_state.active_role = Role.INTERPRETER


def resolve_action(game_state: GameState, action: Action) -> None:
    if action.guess == EndTurn:
        _end_turn(game_state)


def _end_turn(game_state: GameState) -> None:
    game_state.active_team = _get_next_team(game_state)
    game_state.active_role = Role.CODEMASTER
    game_state.guesses_remaining = Quantity(0)


def _get_next_team(game_state: GameState) -> Team:
    teams = game_state.team_outcomes.undetermined
    n_teams = len(teams)
    current_index = teams.index(game_state.active_team)
    next_index = (current_index + 1) % n_teams
    return Team(teams(next_index))
