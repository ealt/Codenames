from codenames.data.codenames_pb2 import Action, Clue
from codenames.data.types import EndTurn, Unlimited
from codenames.game.game_state import GameState


def validate_clue(game_state: GameState, clue: Clue) -> bool:
    if clue.word in game_state.codename_identities:
        return False
    if not (clue.quantity > 0 or clue.quantity == Unlimited):
        return False
    return True


def validate_action(game_state: GameState, action: Action) -> bool:
    if not (action.guess in game_state.codename_identities
            or action.guess == EndTurn):
        return False
    return True
