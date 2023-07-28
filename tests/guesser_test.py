import json

from google.protobuf.json_format import Parse
import pytest

from codenames.data.codenames_pb2 import Action
from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.types import EndTurn
from codenames.data.types import Team
from codenames.data.types import UnknownTeam
from codenames.players.guesser import Guesser
from tests.preprogrammed_guesser import PreprogrammedGuesser


def test_abc_init() -> None:
    with pytest.raises(TypeError):
        _ = Guesser()  # type: ignore


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

GUESS = Parse(json.dumps({'guess': 'cat'}), Action())
END_TURN = Parse(json.dumps({'guess': EndTurn}), Action())


@pytest.mark.parametrize('action', [GUESS, END_TURN], ids=['guess', 'end_turn'])
def test_give_action(action: Action) -> None:
    guesser = PreprogrammedGuesser([action])
    guesser.set_up(Team(1), COMMON_INFORMATION)
    actual_action = guesser.give_action()
    assert actual_action == action
