from collections import defaultdict

from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import SecretInformation
from codenames.data.types import Codename
from codenames.data.types import Information
from codenames.data.types import Team
from codenames.data.types import UnknownTeam
import codenames.data.utils as du
from codenames.game.game_state import GameState


def get_information(game_state: GameState) -> Information:
    common_information = _get_common_information(game_state)
    secret_information = _get_secret_information(game_state)
    return Information(common=common_information, secret=secret_information)


def _get_common_information(game_state: GameState) -> CommonInformation:
    common_information = CommonInformation()
    for team, count in _get_identity_counts(game_state).items():
        common_information.identity_counts[team] = count
    for team, codenames in _get_agent_sets(game_state).items():
        common_information.agent_sets[team].codenames.extend(codenames)
    # turn history cannot be completely inferred from game state
    return common_information


def _get_identity_counts(game_state: GameState) -> dict[Team, int]:
    return {
        team: len(codenames)
        for team, codenames in game_state.unknown_agents.items()
    }


def _get_agent_sets(game_state: GameState) -> dict[Team, list[Codename]]:
    agent_sets: dict[Team, list[Codename]] = defaultdict(list)
    for codename, identity in game_state.codename_identities.items():
        if codename in game_state.unknown_agents[identity]:
            agent_sets[UnknownTeam].append(codename)
        else:
            agent_sets[identity].append(codename)
    return agent_sets


def _get_secret_information(game_state: GameState) -> SecretInformation:
    secret_information = SecretInformation()
    identity_codenames = du.codename_identities_to_identity_codenames(
        game_state.codename_identities
    )
    for team, codenames in identity_codenames.items():
        secret_information.agent_sets[team].codenames.extend(codenames)
    return secret_information
