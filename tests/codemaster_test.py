import json
import unittest

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import (
    Clue, CommonInformation, SecretInformation
)
from codenames.data.types import Team, UnknownTeam, Unlimited
from codenames.players.codemaster import Codemaster
from tests.preprogrammed_codemaster import PreprogrammedCodemaster

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


class CodemasterTest(unittest.TestCase):

    def test_abc_init(self):
        with self.assertRaises(TypeError):
            _ = Codemaster()

    def test_reveal_secret_information(self) -> None:
        codemaster = PreprogrammedCodemaster([])
        codemaster.set_up(Team(1), COMMON_INFORMATION)
        codemaster.reaveal_secret_information(SECRET_INFORMATION)
        self.assertEqual(codemaster._secret_information, SECRET_INFORMATION)

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
