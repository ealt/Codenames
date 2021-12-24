import json

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import CommonInformation, SecretInformation
from codenames.data.utils import codename_identities_to_identity_codenames
from codenames.data.types import Information
from codenames.game.game_state import GameState


def get_information(game_state: GameState) -> Information:
    secret_information = _get_secret_information(game_state)
    common_information = CommonInformation()
    return Information(common=common_information, secret=secret_information)


def _get_secret_information(game_state: GameState) -> SecretInformation:
    identity_codenames = codename_identities_to_identity_codenames(
        game_state.codename_identities
    )
    return Parse(
        json.dumps({'agent_sets': identity_codenames}), SecretInformation()
    )
