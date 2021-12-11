import unittest
from codenames.players.interpreter import Interpreter


class InterpreterTest(unittest.TestCase):

    def test_abc_init(self):
        with self.assertRaises(TypeError):
            _ = Interpreter()


if __name__ == '__main__':
    unittest.main()
