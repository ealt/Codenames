from typing import NewType

from codenames.core.codenames_pb2 import Action, Clue, SharedAction, SharedClue

Team = NewType('Team', int)
UnknownTeam = 0
Codename = NewType('Codename', str)

# protobuf based test data types
TeamClueDict = NewType('TeamClueDict', dict[Team, list[Clue]])
TeamSharedClueDict = NewType('TeamSharedClueDict', dict[Team, list[SharedClue]])
TeamActionDict = NewType('TeamActionDict', dict[Team, list[Action]])
TeamSharedActionDict = NewType('TeamSharedActionDict', dict[Team,
                                                            list[SharedAction]])

# json based test data types
"""
DictClue: {
    'word': str,
    'quantity': int | Unlimited
}

StrAction: Codename | Pass

DictData: {
    'agents': AgentDict,
    'clues': TeamDictClueDict,
    'actions': TeamStrActionDict
}
"""
AgentDict = dict[Team, list[Codename]]
Unlimited = 'unlimited'
DictClue = NewType('DictClue', dict[str, str | int])
TeamDictClueDict = NewType('TeamDictClueDict', dict[Team, list[DictClue]])
Pass = 'pass_'
StrAction = NewType('DictAction', str)
TeamStrActionDict = NewType('TeamStrActionDict', dict[Team, list[StrAction]])
DictData = NewType('DictData',
                   dict[str, AgentDict | TeamDictClueDict | TeamStrActionDict])
