from typing import NewType

from codenames.core.codenames_pb2 import Action, Clue, SharedAction, SharedClue

Team = NewType('Team', int)
UnknownTeam = 0

# TestData Types
TeamClueDict = NewType('TeamClueDict', dict[Team, list[Clue]])
TeamSharedClueDict = NewType('TeamSharedClueDict', dict[Team, list[SharedClue]])
TeamActionDict = NewType('TeamActionDict', dict[Team, list[Action]])
TeamSharedActionDict = NewType('TeamSharedActionDict', dict[Team,
                                                            list[SharedAction]])