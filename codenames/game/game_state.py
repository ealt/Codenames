from dataclasses import dataclass

from codenames.data.codenames_pb2 import Role
from codenames.data.types import (
    CodenameIdentities, IdentityCodenames, Quantity, TeamOutcomes
)
from codenames.game.player_teams import PlayerTeams


@dataclass
class GameState:
    codename_identities: CodenameIdentities
    unknown_agents: IdentityCodenames
    teams: PlayerTeams
    team_outcomes: TeamOutcomes
    active_role: Role
    guesses_remaining: Quantity
