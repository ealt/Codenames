import abc

from codenames.data.codenames_pb2 import Action
from codenames.players.player import Player


class Interpreter(Player):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'give_guess')
            and (callable(subclass.give_guess) or NotImplemented)
        )

    @abc.abstractmethod
    def give_action(self) -> Action:
        pass
