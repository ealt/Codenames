from dataclasses import dataclass, field
from typing import NewType

Team = NewType('Team', int)
NullTeam = Team(0)
NeutralTeam = Team(-1)
AssassinTeam = Team(-2)
UnknownTeam = Team(-3)
NonPlayerTeams = set((UnknownTeam, NeutralTeam, AssassinTeam))
Codename = NewType('Codename', str)
CodenameIdentities = dict[Codename, Team]
IdentityCodenames = dict[Team, set[Codename]]
Quantity = NewType('Quantity', int)
Unlimited = Quantity(-1)
EndTurn = ''


@dataclass
class TeamOutcomes:
    found_agents: list[Team] = field(default_factory=list)
    found_assassin: list[Team] = field(default_factory=list)
