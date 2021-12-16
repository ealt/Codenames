import unittest

from codenames.data.test_data_conversion import convert_to_pb
from codenames.data.types import DictData, Team, UnknownTeam, Unlimited
from codenames.data.utils import get_last_action, get_last_clue
from codenames.players.preprogrammed_codemaster import PreprogrammedCodemaster

TEST_DATA = DictData({
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
})


class PreprogrammedCodemasterTest(unittest.TestCase):

    def setUp(self) -> None:
        test_data = convert_to_pb(TEST_DATA)
        team = Team(1)
        self._codemaster = PreprogrammedCodemaster(test_data.clues[team])
        self.assertEqual(self._codemaster.team, UnknownTeam)
        self._codemaster.set_up(team, test_data.common_information)
        self.assertEqual(self._codemaster.team, team)
        self._codemaster.reaveal_secret_information(
            test_data.secret_information)
        self._shared_clues = test_data.shared_clues
        self._shared_actions = test_data.shared_actions
        self._clues = test_data.clues[team]

    def test_recieve_clue(self) -> None:
        for team_shared_clues in self._shared_clues.values():
            for shared_clue in team_shared_clues:
                self._codemaster.reveal_clue(shared_clue)
                self.assertEqual(
                    get_last_clue(self._codemaster._common_information),
                    shared_clue)

    def test_reveal_action(self) -> None:
        for team_shared_actions in self._shared_actions.values():
            for shared_action in team_shared_actions:
                self._codemaster.reveal_action(shared_action)
                self.assertEqual(
                    get_last_action(self._codemaster._common_information),
                    shared_action)

    def test_give_clue(self) -> None:
        for expected_clue in self._clues:
            actual_clue = self._codemaster.give_clue()
            self.assertEqual(actual_clue, expected_clue)


if __name__ == '__main__':
    unittest.main()
