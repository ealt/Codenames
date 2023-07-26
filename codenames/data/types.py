from dataclasses import dataclass
from dataclasses import field
from typing import NamedTuple, NewType

from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import SecretInformation

Team = NewType('Team', int)
NullTeam = Team(0)
NeutralTeam = Team(-1)
AssassinTeam = Team(-2)
UnknownTeam = Team(-3)
NonPlayerTeams = set((UnknownTeam, NeutralTeam, AssassinTeam))

Codename = NewType('Codename', str)
EndTurn = ''

Quantity = NewType('Quantity', int)
Unlimited = Quantity(-1)

CodenameIdentities = dict[Codename, Team]
IdentityCodenames = dict[Team, set[Codename]]


@dataclass
class TeamOutcomes:
    found_agents: list[Team] = field(default_factory=list)
    found_assassin: list[Team] = field(default_factory=list)


class Information(NamedTuple):
    common: CommonInformation
    secret: SecretInformation
