import json

from google.protobuf.json_format import Parse
import pytest

from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import SharedAction
from codenames.data.codenames_pb2 import SharedClue
from codenames.data.types import EndTurn
from codenames.data.types import Team
from codenames.data.types import UnknownTeam
from codenames.data.types import Unlimited
import codenames.data.utils as du
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


def test_set_up() -> None:
    player = Player()
    assert player.team == UnknownTeam
    player.set_up(Team(1), COMMON_INFORMATION)
    assert player.team == Team(1)


FINITE_CLUE = Parse(
    json.dumps({
        'team': 1,
        'clue': {
            'word': 'meow',
            'quantity': 1
        }
    }), SharedClue()
)

UNLIMITED_CLUE = Parse(
    json.dumps({
        'team': 1,
        'clue': {
            'word': 'wiskers',
            'quantity': Unlimited
        }
    }), SharedClue()
)


@pytest.mark.parametrize(
    'shared_clue', [FINITE_CLUE, UNLIMITED_CLUE], ids=['finite', 'unlmited']
)
def test_reveal_clue(shared_clue: SharedClue) -> None:
    player = Player()
    player.set_up(Team(1), COMMON_INFORMATION)
    player.reveal_clue(shared_clue)
    assert du.get_last_clue(player._common_information) == shared_clue


GUESS = Parse(
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

END_TURN = Parse(
    json.dumps({
        'team': 1,
        'action': {
            'guess': EndTurn
        }
    }), SharedAction()
)


@pytest.mark.parametrize(
    'shared_action', [GUESS, END_TURN], ids=['guess', 'end_turn']
)
def test_reveal_action(shared_action: SharedAction) -> None:
    player = Player()
    player.set_up(Team(1), COMMON_INFORMATION)
    player.reveal_action(shared_action)
    assert du.get_last_action(player._common_information) == shared_action
