from dataclasses import dataclass
from dataclasses import field
from typing import NewType

Team = NewType('Team', int)
NullTeam = Team(0)
NeutralTeam = Team(-1)
FatalTeam = Team(-2)
UnknownTeam = Team(-3)
NonPlayerTeams = set((UnknownTeam, NeutralTeam, FatalTeam))

Codename = NewType('Codename', str)
EndTurn = ''

Quantity = NewType('Quantity', int)
Unlimited = Quantity(-1)

CodenameIdentities = dict[Codename, Team]
IdentityCodenames = dict[Team, set[Codename]]


@dataclass
class TeamOutcomes:
    found_agents: list[Team] = field(default_factory=list)
    found_fatal: list[Team] = field(default_factory=list)
