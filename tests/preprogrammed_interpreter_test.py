import unittest

from codenames.data.test_data_conversion import convert_to_pb
from codenames.data.types import Pass, UnknownTeam
from codenames.data.utils import get_last_action, get_last_clue
from codenames.players.preprogrammed_interpreter import \
    PreprogrammedInterpreter

TEST_DATA = {
    'agents': {
        0: ['cat'],
        1: ['dog'],
    },
    'clues': {
        0: [{
            'word': 'meow',
            'quantity': 1
        }]
    },
    'actions': {
        0: ['cat', Pass]
    },
}


class PreprogrammedInterpreterTest(unittest.TestCase):

    def setUp(self) -> None:
        test_data = convert_to_pb(TEST_DATA)
        self._interpreter = PreprogrammedInterpreter()
        self.assertEqual(self._interpreter.team, UnknownTeam)
        self._interpreter.set_up(0, test_data.common_information,
                                 test_data.actions[0])
        self.assertEqual(self._interpreter.team, 0)
        self._shared_clues = test_data.shared_clues
        self._shared_actions = test_data.shared_actions
        self._actions = test_data.actions[0]

    def test_recieve_clue(self) -> None:
        for team_shared_clues in self._shared_clues.values():
            for shared_clue in team_shared_clues:
                self._interpreter.reveal_clue(shared_clue)
                self.assertEqual(
                    get_last_clue(self._interpreter._common_information),
                    shared_clue)

    def test_reveal_action(self) -> None:
        for team_shared_actions in self._shared_actions.values():
            for shared_action in team_shared_actions:
                self._interpreter.reveal_action(shared_action)
                self.assertEqual(
                    get_last_action(self._interpreter._common_information),
                    shared_action)

    def test_give_action(self) -> None:
        for expected_action in self._actions:
            actual_action = self._interpreter.give_action()
            self.assertEqual(actual_action, expected_action)


if __name__ == '__main__':
    unittest.main()
