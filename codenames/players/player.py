import abc

from codenames.data.codenames_pb2 import (
    CommonInformation, SharedAction, SharedClue
)
from codenames.data.types import Team, UnknownTeam
from codenames.data.utils import (
    update_informaiton_with_action, update_information_with_clue
)


class Player(abc.ABC):

    def __init__(self) -> None:
        self._team = UnknownTeam

    @property
    def team(self) -> Team:
        return self._team

    def set_up(self, team: Team, common_information: CommonInformation) -> None:
        self._team = team
        self._common_information = common_information

    def reveal_clue(self, shared_clue: SharedClue) -> None:
        update_information_with_clue(self._common_information, shared_clue)

    def reveal_action(self, shared_action: SharedAction) -> None:
        update_informaiton_with_action(self._common_information, shared_action)
