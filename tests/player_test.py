import json
import unittest

from google.protobuf.json_format import Parse

from codenames.data.codenames_pb2 import (
    CommonInformation, SharedAction, SharedClue
)
from codenames.data.types import EndTurn, Team, UnknownTeam, Unlimited
from codenames.data.utils import get_last_action, get_last_clue
from codenames.players.player import Player

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


class PlayerTest(unittest.TestCase):

    def test_set_up(self) -> None:
        player = Player()
        self.assertEqual(player.team, UnknownTeam)
        player.set_up(Team(1), COMMON_INFORMATION)
        self.assertEqual(player.team, Team(1))

    def test_reveal_finite_clue(self) -> None:
        player = Player()
        player.set_up(Team(1), COMMON_INFORMATION)
        shared_clue = Parse(
            json.dumps({
                'team': 1,
                'clue': {
                    'word': 'meow',
                    'quantity': 1
                }
            }), SharedClue()
        )
        player.reveal_clue(shared_clue)
        self.assertEqual(get_last_clue(player._common_information), shared_clue)

    def test_reveal_unlimited_clue(self) -> None:
        player = Player()
        player.set_up(Team(1), COMMON_INFORMATION)
        shared_clue = Parse(
            json.dumps({
                'team': 1,
                'clue': {
                    'word': 'wiskers',
                    'quantity': Unlimited
                }
            }), SharedClue()
        )
        player.reveal_clue(shared_clue)
        self.assertEqual(get_last_clue(player._common_information), shared_clue)

    def test_reveal_guess(self) -> None:
        player = Player()
        player.set_up(Team(1), COMMON_INFORMATION)
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
        player.reveal_action(shared_action)
        self.assertEqual(
            get_last_action(player._common_information), shared_action
        )

    def test_reveal_end_turn(self) -> None:
        player = Player()
        player.set_up(Team(1), COMMON_INFORMATION)
        shared_action = Parse(
            json.dumps({
                'team': 1,
                'action': {
                    'guess': EndTurn
                }
            }), SharedAction()
        )
        player.reveal_action(shared_action)
        self.assertEqual(
            get_last_action(player._common_information), shared_action
        )


if __name__ == '__main__':
    unittest.main()
