import unittest

from codenames.data.test_data_conversion import convert_to_pb
from codenames.data.types import EndTurn, Team, UnknownTeam
from codenames.data.utils import get_last_action, get_last_clue
from codenames.players.preprogrammed_interpreter import \
    PreprogrammedInterpreter

TEST_DATA = {
    'agents': {
        1: ['cat'],
        2: ['dog'],
    },
    'turns': [{
        'team': 1,
        'clue': {
            'word': 'meow',
            'quantity': 1
        },
        'actions': ['cat', EndTurn]
    }]
}


class PreprogrammedInterpreterTest(unittest.TestCase):

    def setUp(self) -> None:
        test_data = convert_to_pb(TEST_DATA)  # type: ignore
        self._turns = test_data.common_information.turn_history
        test_data.common_information.ClearField('turn_history')
        team = Team(1)
        self._interpreter = PreprogrammedInterpreter(test_data.actions[team])
        self.assertEqual(self._interpreter.team, UnknownTeam)
        self._interpreter.set_up(team, test_data.common_information)
        self.assertEqual(self._interpreter.team, team)
        self._actions = test_data.actions[team]

    def test_recieve_clue(self) -> None:
        for turn in self._turns:
            shared_clue = turn.clue
            self._interpreter.reveal_clue(shared_clue)
            self.assertEqual(
                get_last_clue(self._interpreter._common_information),
                shared_clue
            )

    def test_reveal_action(self) -> None:
        for turn in self._turns:
            for shared_action in turn.actions:
                self._interpreter.reveal_action(shared_action)
                self.assertEqual(
                    get_last_action(self._interpreter._common_information),
                    shared_action
                )

    def test_give_action(self) -> None:
        for expected_action in self._actions:
            actual_action = self._interpreter.give_action()
            self.assertEqual(actual_action, expected_action)


if __name__ == '__main__':
    unittest.main()
