import unittest

from codenames.players.player import Player


class PlayerTest(unittest.TestCase):

    def test_abc_init(self):
        with self.assertRaises(TypeError):
            _ = Player()


if __name__ == '__main__':
    unittest.main()
