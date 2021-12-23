import unittest

from codenames.data.test_data_conversion import convert_to_pb
from codenames.data.types import Team, UnknownTeam, Unlimited
from codenames.data.utils import get_last_action, get_last_clue
from codenames.players.preprogrammed_codemaster import PreprogrammedCodemaster

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
        'actions': ['cat']
    }, {
        'team': 1,
        'clue': {
            'word': 'wiskers',
            'quantity': Unlimited
        },
        'actions': []
    }]
}


class PreprogrammedCodemasterTest(unittest.TestCase):

    def setUp(self) -> None:
        test_data = convert_to_pb(TEST_DATA)  # type: ignore
        self._turns = test_data.common_information.turn_history
        test_data.common_information.ClearField('turn_history')
        team = Team(1)
        self._codemaster = PreprogrammedCodemaster(test_data.clues[team])
        self.assertEqual(self._codemaster.team, UnknownTeam)
        self._codemaster.set_up(team, test_data.common_information)
        self.assertEqual(self._codemaster.team, team)
        self._codemaster.reaveal_secret_information(
            test_data.secret_information
        )
        self._clues = test_data.clues[team]

    def test_recieve_clue(self) -> None:
        for turn in self._turns:
            shared_clue = turn.clue
            self._codemaster.reveal_clue(shared_clue)
            self.assertEqual(
                get_last_clue(self._codemaster._common_information), shared_clue
            )

    def test_reveal_action(self) -> None:
        for turn in self._turns:
            for shared_action in turn.actions:
                self._codemaster.reveal_action(shared_action)
                self.assertEqual(
                    get_last_action(self._codemaster._common_information),
                    shared_action
                )

    def test_give_clue(self) -> None:
        for expected_clue in self._clues:
            actual_clue = self._codemaster.give_clue()
            self.assertEqual(actual_clue, expected_clue)


if __name__ == '__main__':
    unittest.main()
