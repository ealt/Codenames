import abc

from codenames.data.codenames_pb2 import (Clue, CommonInformation,
                                          SecretInformation)
from codenames.data.types import Team
from codenames.players.player import Player


class Codemaster(Player):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'give_clue') and
                (callable(subclass.give_clue) or NotImplemented))

    def set_up(self, team: Team, common_information: CommonInformation):
        super().set_up(team, common_information)

    def reaveal_secret_information(
            self, secret_information: SecretInformation) -> None:
        self._secret_information = secret_information

    @abc.abstractmethod
    def give_clue(self) -> Clue:
        pass
