from dataclasses import dataclass

from codenames.data.types import CodenameIdentities
from codenames.data.types import IdentityCodenames
from codenames.data.types import Quantity
from codenames.data.types import TeamOutcomes
from codenames.game.player_teams import PlayerTeams


@dataclass
class GameState:
    codename_identities: CodenameIdentities
    unknown_agents: IdentityCodenames
    teams: PlayerTeams
    team_outcomes: TeamOutcomes
    active_role: int
    guesses_remaining: Quantity
