import json
import pytest

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import Action, CommonInformation
from codenames.data.types import EndTurn, Team, UnknownTeam
from codenames.players.interpreter import Interpreter
from tests.preprogrammed_interpreter import \
    PreprogrammedInterpreter


def test_abc_init():
    with pytest.raises(TypeError):
        _ = Interpreter()


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
def test_give_action(action) -> None:
    interpreter = PreprogrammedInterpreter([action])
    interpreter.set_up(Team(1), COMMON_INFORMATION)
    actual_action = interpreter.give_action()
    assert actual_action == action
