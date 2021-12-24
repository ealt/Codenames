import json

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import CommonInformation, SecretInformation
from codenames.data.utils import codename_identities_to_identity_codenames
from codenames.data.types import Information, Team
from codenames.game.game_state import GameState


def get_information(game_state: GameState) -> Information:
    common_information = _get_common_information(game_state)
    secret_information = _get_secret_information(game_state)
    return Information(common=common_information, secret=secret_information)


def _get_secret_information(game_state: GameState) -> SecretInformation:
    identity_codenames = codename_identities_to_identity_codenames(
        game_state.codename_identities
    )
    return Parse(
        json.dumps({'agent_sets': identity_codenames}), SecretInformation()
    )


def _get_common_information(game_state: GameState) -> CommonInformation:
    return Parse(
        json.dumps({
            'identity_counts': _get_identity_counts(game_state),
            'agent_sets': {},
            'turn_history': [],
        }), CommonInformation()
    )


def _get_identity_counts(game_state: GameState) -> dict[Team, int]:
    return {
        team: len(codenames)
        for team, codenames in game_state.unknown_agents.items()
    }
