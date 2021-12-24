from codenames.data.codenames_pb2 import Action
from codenames.players.interpreter import Interpreter


class PreprogrammedInterpreter(Interpreter):

    def __init__(self, actions: list[Action]) -> None:
        super().__init__()
        self._actions = list(reversed(actions))

    def give_action(self) -> Action:
        action = self._actions.pop()
        return action
