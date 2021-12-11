import abc

from codenames.core.codenames_pb2 import SharedAction, SharedClue


class Player(abc.ABC):

    @abc.abstractmethod
    def set_up(self, team: int) -> None:
        self._team = team

    def reveal_clue(self, shared_clue: SharedClue) -> None:
        pass

    def reveal_action(self, shared_action: SharedAction) -> None:
        pass