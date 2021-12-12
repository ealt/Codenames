import unittest

from codenames.data.test_data_conversion import convert_to_pb
from codenames.data.types import UnknownTeam, Unlimited
from codenames.players.preprogrammed_codemaster import PreprogrammedCodemaster

TEST_DATA = {
    'agents': {
        1: ['cat'],
        2: ['dog'],
    },
    'clues': {
        1: [{
            'word': 'meow',
            'quantity': 1
        }, {
            'word': 'wiskers',
            'quantity': Unlimited
        }]
    },
    'actions': {
        1: ['cat']
    },
}


class PreprogrammedCodemasterTest(unittest.TestCase):

    def setUp(self) -> None:
        test_data = convert_to_pb(TEST_DATA)
        self._codemaster = PreprogrammedCodemaster()
        self.assertEqual(self._codemaster.team, UnknownTeam)
        self._codemaster.set_up(1, test_data.secret_information,
                                test_data.clues[1])
        self.assertEqual(self._codemaster.team, 1)
        self._shared_clues = test_data.shared_clues
        self._shared_actions = test_data.shared_actions
        self._clues = test_data.clues[1]

    def test_recieve_clue(self) -> None:
        for team_shared_clues in self._shared_clues.values():
            for shared_clue in team_shared_clues:
                self._codemaster.reveal_clue(shared_clue)

    def test_reveal_action(self) -> None:
        for team_shared_actions in self._shared_actions.values():
            for shared_action in team_shared_actions:
                self._codemaster.reveal_action(shared_action)

    def test_give_clue(self) -> None:
        for expected_clue in self._clues:
            actual_clue = self._codemaster.give_clue()
            self.assertEqual(actual_clue, expected_clue)


if __name__ == '__main__':
    unittest.main()