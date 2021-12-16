from dataclasses import dataclass

from codenames.data.codenames_pb2 import CommonInformation, SecretInformation
from codenames.data.types import (
    TeamActionDict, TeamClueDict, TeamSharedActionDict, TeamSharedClueDict
)


@dataclass
class TestData:
    secret_information: SecretInformation
    common_information: CommonInformation
    clues: TeamClueDict
    shared_clues: TeamSharedClueDict
    actions: TeamActionDict
    shared_actions: TeamSharedActionDict
