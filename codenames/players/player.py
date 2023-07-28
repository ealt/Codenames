import abc

from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import SharedAction
from codenames.data.codenames_pb2 import SharedClue
from codenames.data.types import Team
from codenames.data.types import UnknownTeam
import codenames.data.utils as du


class Player(abc.ABC):

    def __init__(self) -> None:
        self._team = UnknownTeam

    @property
    def team(self) -> Team:
        return self._team

    def set_up(self, team: Team, common_information: CommonInformation) -> None:
        self._team = team
        self._common_information = CommonInformation()
        self._common_information.CopyFrom(common_information)

    def reveal_clue(self, shared_clue: SharedClue) -> None:
        du.update_information_with_clue(self._common_information, shared_clue)

    def reveal_action(self, shared_action: SharedAction) -> None:
        du.update_information_with_action(self._common_information, shared_action)
