import unittest
from codenames.core.codenames_pb2 import SecretInformation
from codenames.players.codemaster import Codemaster


class CodemasterTest(unittest.TestCase):

    def test_abc_init(self):
        with self.assertRaises(TypeError):
            secret_information = SecretInformation()
            _ = Codemaster()


if __name__ == '__main__':
    unittest.main()
