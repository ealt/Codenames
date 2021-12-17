from dataclasses import dataclass

from codenames.data.codenames_pb2 import Role
from codenames.data.types import (
    CodenameIdentities, IdentityCodenames, Quantity, Team, TeamOutcomes
)


@dataclass
class GameState:
    codename_identities: CodenameIdentities
    unknown_agents: IdentityCodenames
    team_outcomes: TeamOutcomes
    active_team: Team
    active_role: Role
    guesses_remaining: Quantity
