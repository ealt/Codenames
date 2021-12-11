import abc

from codenames.core.codenames_pb2 import Clue, SecretInformation
from codenames.players.player import Player


class Codemaster(Player):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'give_clue') and
                (callable(subclass.give_clue) or NotImplemented))

    def set_up(self, team: int, secret_information: SecretInformation):
        super().set_up(team)
        self._secret_information = secret_information

    @abc.abstractmethod
    def give_clue(self) -> Clue:
        pass