from codenames.data.codenames_pb2 import Action, CommonInformation
from codenames.data.types import Team
from codenames.players.interpreter import Interpreter


class PreprogrammedInterpreter(Interpreter):

    def set_up(self, team: Team, common_information: CommonInformation,
               actions: list[Action]) -> None:
        super().set_up(team, common_information)
        self._actions = list(reversed(actions))

    def give_action(self) -> Action:
        action = self._actions.pop()
        return action