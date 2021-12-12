import abc

from codenames.data.codenames_pb2 import SharedAction, SharedClue
from codenames.data.types import Team, UnknownTeam


class Player(abc.ABC):

    def __init__(self) -> None:
        self._team = UnknownTeam

    @property
    def team(self) -> Team:
        return self._team

    @abc.abstractmethod
    def set_up(self, team: Team) -> None:
        self._team = team

    def reveal_clue(self, shared_clue: SharedClue) -> None:
        pass

    def reveal_action(self, shared_action: SharedAction) -> None:
        pass