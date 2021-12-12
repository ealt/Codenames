import abc

from codenames.core.codenames_pb2 import SharedAction, SharedClue
from codenames.core.types import Team


class Player(abc.ABC):

    @abc.abstractmethod
    def set_up(self, team: Team) -> None:
        self._team = team

    def reveal_clue(self, shared_clue: SharedClue) -> None:
        pass

    def reveal_action(self, shared_action: SharedAction) -> None:
        pass