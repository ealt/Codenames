import abc

from codenames.data.codenames_pb2 import CommonInformation, SharedAction, SharedClue
from codenames.data.types import Team, UnknownTeam


class Player(abc.ABC):

    def __init__(self) -> None:
        self._team = UnknownTeam

    @property
    def team(self) -> Team:
        return self._team

    @abc.abstractmethod
    def set_up(self, team: Team, common_information: CommonInformation) -> None:
        self._team = team
        self._common_information = common_information

    def reveal_clue(self, shared_clue: SharedClue) -> None:
        pass

    def reveal_action(self, shared_action: SharedAction) -> None:
        pass