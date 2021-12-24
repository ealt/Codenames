import json
import unittest

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import Action, CommonInformation
from codenames.data.types import EndTurn, Team, UnknownTeam
from codenames.players.interpreter import Interpreter
from tests.preprogrammed_interpreter import \
    PreprogrammedInterpreter

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


class InterpreterTest(unittest.TestCase):

    def test_abc_init(self):
        with self.assertRaises(TypeError):
            _ = Interpreter()

    def test_give_guess(self) -> None:
        guess = Parse(json.dumps({'guess': 'cat'}), Action())
        interpreter = PreprogrammedInterpreter([guess])
        interpreter.set_up(Team(1), COMMON_INFORMATION)
        actual_action = interpreter.give_action()
        self.assertEqual(actual_action, guess)

    def test_end_turn(self) -> None:
        end_turn = Parse(json.dumps({'guess': EndTurn}), Action())
        interpreter = PreprogrammedInterpreter([end_turn])
        interpreter.set_up(Team(1), COMMON_INFORMATION)
        actual_action = interpreter.give_action()
        self.assertEqual(actual_action, end_turn)


if __name__ == '__main__':
    unittest.main()
