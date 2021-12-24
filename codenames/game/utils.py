from codenames.data.codenames_pb2 import CommonInformation, SecretInformation
from codenames.data.types import Information
from codenames.game.game_state import GameState


def get_information(game_state: GameState) -> Information:
    secret_information = SecretInformation()
    common_information = CommonInformation()
    return Information(common=common_information, secret=secret_information)
