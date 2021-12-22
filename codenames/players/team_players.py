from typing import NamedTuple

from codenames.players.codemaster import Codemaster
from codenames.players.interpreter import Interpreter


class TeamPlayers(NamedTuple):
    codemaster: Codemaster
    interpreter: Interpreter
