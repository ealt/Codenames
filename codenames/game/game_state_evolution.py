from codenames.data.codenames_pb2 import Clue, Role
from codenames.data.types import Quantity
from codenames.game.game_state import GameState


def resolve_clue(game_state: GameState, clue: Clue) -> None:
    game_state.guesses_remaining = Quantity(clue.quantity)
    game_state.active_role = Role.INTERPRETER
