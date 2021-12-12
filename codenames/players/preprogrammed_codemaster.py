from codenames.data.codenames_pb2 import Clue, SecretInformation
from codenames.players.codemaster import Codemaster


class PreprogrammedCodemaster(Codemaster):

    def set_up(self, team: int, secret_information: SecretInformation,
               clues: list[Clue]) -> None:
        super().set_up(team, secret_information)
        self._clues = list(reversed(clues))

    def give_clue(self) -> Clue:
        clue = self._clues.pop()
        return clue