from codenames.data.codenames_pb2 import Action
from codenames.players.guesser import Guesser


class PreprogrammedGuesser(Guesser):

    def __init__(self, actions: list[Action]) -> None:
        super().__init__()
        self._actions = list(reversed(actions))

    def give_action(self) -> Action:
        action = self._actions.pop()
        return action
