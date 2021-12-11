import abc

from codenames.core.codenames_pb2 import Action, CommonInformation
from codenames.players.player import Player


class Interpreter(Player):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'give_guess') and
                (callable(subclass.give_guess) or NotImplemented))

    def set_up(self, team: int, common_information: CommonInformation):
        super().set_up(team)
        self._common_information = common_information

    @abc.abstractmethod
    def give_action(self) -> Action:
        pass