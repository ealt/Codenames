from codenames.data.codenames_pb2 import Clue
from codenames.players.codemaster import Codemaster


class PreprogrammedCodemaster(Codemaster):

    def __init__(self, clues: list[Clue]) -> None:
        super().__init__()
        self._clues = list(reversed(clues))

    def give_clue(self) -> Clue:
        clue = self._clues.pop()
        return clue
