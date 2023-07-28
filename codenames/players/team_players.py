from typing import NamedTuple

from codenames.players.clue_giver import ClueGiver
from codenames.players.guesser import Guesser


class TeamPlayers(NamedTuple):
    clue_giver: ClueGiver
    guesser: Guesser
