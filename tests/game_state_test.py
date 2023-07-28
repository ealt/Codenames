from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import Role
from codenames.data.codenames_pb2 import SecretInformation
from codenames.data.types import Codename
from codenames.data.types import CodenameIdentities
from codenames.data.types import IdentityCodenames
from codenames.data.types import NeutralTeam
from codenames.data.types import Quantity
from codenames.data.types import Team
from codenames.data.types import TeamOutcomes
from codenames.data.types import UnknownTeam
from codenames.game.game_state import GameState
from codenames.game.player_team_list import PlayerTeamList

SECRET_INFO = SecretInformation()
SECRET_INFO.agent_sets[1].codenames.extend(['calico', 'siamese', 'tabby'])
SECRET_INFO.agent_sets[2].codenames.extend(['husky', 'corgi', 'labrador'])
SECRET_INFO.agent_sets[NeutralTeam].codenames.extend(['bird'])

COMMON_INFO = CommonInformation()
COMMON_INFO.identity_counts[1] = 1
COMMON_INFO.identity_counts[2] = 2
COMMON_INFO.identity_counts[NeutralTeam] = 1
COMMON_INFO.agent_sets[UnknownTeam].codenames.extend([
    'tabby', 'corgi', 'husky', 'bird'
])
COMMON_INFO.agent_sets[1].codenames.extend(['siamese', 'calico'])
COMMON_INFO.agent_sets[2].codenames.extend([
    'labrador',
])

GAME_STATE = GameState(
    codename_identities=CodenameIdentities({
        Codename(codename): Team(identity)
        for codename, identity in [('tabby', 1), ('siamese', 1), ('calico', 1),
                                   ('labrador',
                                    2), ('corgi',
                                         2), ('husky',
                                              2), ('bird', NeutralTeam)]
    }),
    unknown_agents=IdentityCodenames({
        Team(1): set([Codename('tabby')]),
        Team(2): set(map(Codename, ['corgi', 'husky'])),
        NeutralTeam: set([Codename('bird')]),
    }),
    player_teams=PlayerTeamList([Team(1), Team(2)]),
    team_outcomes=TeamOutcomes(),
    active_role=Role.CLUE_GIVER,
    guesses_remaining=Quantity(0)
)


def test_get_setcret_information() -> None:
    secret_information = GAME_STATE.get_secret_information()
    assert set(secret_information.agent_sets.keys()) == set(
        SECRET_INFO.agent_sets.keys()
    )
    for key in SECRET_INFO.agent_sets.keys():
        assert set(secret_information.agent_sets[key].codenames) == set(
            SECRET_INFO.agent_sets[key].codenames
        )


def test_get_common_information() -> None:
    common_information = GAME_STATE.get_common_information()
    assert common_information.SerializeToString(
        deterministic=True
    ) == COMMON_INFO.SerializeToString(deterministic=True)
