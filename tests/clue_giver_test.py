import json

from google.protobuf.json_format import Parse
import pytest

from codenames.data.codenames_pb2 import Clue
from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import SecretInformation
from codenames.data.types import Team
from codenames.data.types import UnknownTeam
from codenames.data.types import Unlimited
from codenames.players.clue_giver import ClueGiver
from tests.preprogrammed_clue_giver import PreprogrammedClueGiver


def test_abc_init() -> None:
    with pytest.raises(TypeError):
        _ = ClueGiver()  # type: ignore


SECRET_INFORMATION = Parse(
    json.dumps({
        'agent_sets': {
            1: {
                'codenames': ['cat']
            },
            2: {
                'codenames': ['dog']
            }
        }
    }), SecretInformation()
)

COMMON_INFORMATION = Parse(
    json.dumps({
        'identity_counts': {
            1: 1,
            2: 1
        },
        'agent_sets': {
            UnknownTeam: {
                'codenames': ['cat', 'dog']
            }
        },
        'turn_history': []
    }), CommonInformation()
)


def test_reveal_secret_information() -> None:
    clue_giver = PreprogrammedClueGiver([])
    clue_giver.set_up(Team(1), COMMON_INFORMATION)
    clue_giver.reaveal_secret_information(SECRET_INFORMATION)
    assert clue_giver._secret_information == SECRET_INFORMATION


FINITE_CLUE = Parse(json.dumps({'word': 'meow', 'quantity': 1}), Clue())
UNLIMITED_CLUE = Parse(
    json.dumps({
        'word': 'wiskers',
        'quantity': Unlimited
    }), Clue()
)


@pytest.mark.parametrize(
    'clue', [FINITE_CLUE, UNLIMITED_CLUE], ids=['finite', 'unlmited']
)
def test_give_clue(clue: Clue) -> None:
    clue_giver = PreprogrammedClueGiver([clue])
    clue_giver.set_up(Team(1), COMMON_INFORMATION)
    actual_clue = clue_giver.give_clue()
    assert actual_clue == clue
