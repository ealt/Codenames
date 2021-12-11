import unittest
from codenames.players.codemaster import Codemaster


class CodemasterTest(unittest.TestCase):

    def test_abc_init(self):
        with self.assertRaises(TypeError):
            _ = Codemaster()


if __name__ == '__main__':
    unittest.main()
