import json
import unittest

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import (
    Clue, CommonInformation, SecretInformation, SharedAction, SharedClue
)
from codenames.data.types import EndTurn, Team, UnknownTeam, Unlimited
from codenames.data.utils import get_last_action, get_last_clue
from codenames.players.preprogrammed_codemaster import PreprogrammedCodemaster

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


class PreprogrammedCodemasterTest(unittest.TestCase):

    def test_set_up(self) -> None:
        codemaster = PreprogrammedCodemaster([])
        self.assertEqual(codemaster.team, UnknownTeam)
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        self.assertEqual(codemaster.team, Team(1))

    def test_reveal_secret_information(self) -> None:
        codemaster = PreprogrammedCodemaster([])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        codemaster.reaveal_secret_information(SECRET_INFORMATION)
        self.assertEqual(codemaster._secret_information, SECRET_INFORMATION)

    def test_reveal_finite_clue(self) -> None:
        codemaster = PreprogrammedCodemaster([])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        shared_clue = Parse(
            json.dumps({
                'team': 1,
                'clue': {
                    'word': 'meow',
                    'quantity': 1
                }
            }), SharedClue()
        )
        codemaster.reveal_clue(shared_clue)
        self.assertEqual(
            get_last_clue(codemaster._common_information), shared_clue
        )

    def test_reveal_unlimited_clue(self) -> None:
        codemaster = PreprogrammedCodemaster([])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        shared_clue = Parse(
            json.dumps({
                'team': 1,
                'clue': {
                    'word': 'wiskers',
                    'quantity': Unlimited
                }
            }), SharedClue()
        )
        codemaster.reveal_clue(shared_clue)
        self.assertEqual(
            get_last_clue(codemaster._common_information), shared_clue
        )

    def test_reveal_guess(self) -> None:
        codemaster = PreprogrammedCodemaster([])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
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
        codemaster.reveal_action(shared_action)
        self.assertEqual(
            get_last_action(codemaster._common_information), shared_action
        )

    def test_reveal_end_turn(self) -> None:
        codemaster = PreprogrammedCodemaster([])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        shared_action = Parse(
            json.dumps({
                'team': 1,
                'action': {
                    'guess': EndTurn
                }
            }), SharedAction()
        )
        codemaster.reveal_action(shared_action)
        self.assertEqual(
            get_last_action(codemaster._common_information), shared_action
        )

    def test_give_finite_clue(self) -> None:
        clue = Parse(json.dumps({'word': 'meow', 'quantity': 1}), Clue())
        codemaster = PreprogrammedCodemaster([clue])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        actual_clue = codemaster.give_clue()
        self.assertEqual(actual_clue, clue)

    def test_give_unlimited_clue(self) -> None:
        clue = Parse(
            json.dumps({
                'word': 'wiskers',
                'quantity': Unlimited
            }), Clue()
        )
        codemaster = PreprogrammedCodemaster([clue])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        actual_clue = codemaster.give_clue()
        self.assertEqual(actual_clue, clue)


if __name__ == '__main__':
    unittest.main()
