import json
import unittest

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import (
    Action, CommonInformation, SharedAction, SharedClue
)
from codenames.data.types import EndTurn, Team, UnknownTeam, Unlimited
from codenames.data.utils import get_last_action, get_last_clue
from codenames.players.preprogrammed_interpreter import \
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


class PreprogrammedInterpreterTest(unittest.TestCase):

    def test_set_up(self) -> None:
        interpreter = PreprogrammedInterpreter([])
        self.assertEqual(interpreter.team, UnknownTeam)
        interpreter.set_up(Team(1), COMMON_INFORMATION)
        self.assertEqual(interpreter.team, Team(1))

    def test_reveal_finite_clue(self) -> None:
        interpreter = PreprogrammedInterpreter([])
        interpreter.set_up(Team(1), COMMON_INFORMATION)
        shared_clue = Parse(
            json.dumps({
                'team': 1,
                'clue': {
                    'word': 'meow',
                    'quantity': 1
                }
            }), SharedClue()
        )
        interpreter.reveal_clue(shared_clue)
        self.assertEqual(
            get_last_clue(interpreter._common_information), shared_clue
        )

    def test_reveal_unlimited_clue(self) -> None:
        interpreter = PreprogrammedInterpreter([])
        interpreter.set_up(Team(1), COMMON_INFORMATION)
        shared_clue = Parse(
            json.dumps({
                'team': 1,
                'clue': {
                    'word': 'wiskers',
                    'quantity': Unlimited
                }
            }), SharedClue()
        )
        interpreter.reveal_clue(shared_clue)
        self.assertEqual(
            get_last_clue(interpreter._common_information), shared_clue
        )

    def test_reveal_guess(self) -> None:
        interpreter = PreprogrammedInterpreter([])
        interpreter.set_up(Team(1), COMMON_INFORMATION)
        shared_action = Parse(
            json.dumps({
                'team': 1,
                'action': {
                    'guess': 'cat'
                },
                'action_outcome': {
                    'identity': 1
                }
            }), SharedAction()
        )
        interpreter.reveal_action(shared_action)
        self.assertEqual(
            get_last_action(interpreter._common_information), shared_action
        )

    def test_reveal_end_turn(self) -> None:
        interpreter = PreprogrammedInterpreter([])
        interpreter.set_up(Team(1), COMMON_INFORMATION)
        shared_action = Parse(
            json.dumps({
                'team': 1,
                'action': {
                    'guess': EndTurn
                }
            }), SharedAction()
        )
        interpreter.reveal_action(shared_action)
        self.assertEqual(
            get_last_action(interpreter._common_information), shared_action
        )

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
