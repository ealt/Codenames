from dataclasses import dataclass, field
from typing import NewType, TypedDict

from codenames.data.codenames_pb2 import Action, Clue

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


# protobuf based test data types
TeamClueDict = NewType('TeamClueDict', dict[Team, list[Clue]])
TeamActionDict = NewType('TeamActionDict', dict[Team, list[Action]])

# json based test data types
AgentDict = dict[Team, list[Codename]]


class DictClue(TypedDict):
    word: str
    quantity: Quantity


StrAction = NewType('StrAction', str)


class DictTurn(TypedDict):
    team: Team
    clue: DictClue
    actions: list[StrAction]


class DictData(TypedDict):
    agents: AgentDict
    turns: list[DictTurn]
