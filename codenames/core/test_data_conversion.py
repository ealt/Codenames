from typing import Optional

from codenames.core.codenames_pb2 import (Clue, CommonInformation,
                                          SecretInformation, SharedClue)

from codenames.core.types import (AgentDict, Codename, DictData, TeamClueDict,
                                  TeamDictClueDict, TeamSharedClueDict,
                                  UnknownTeam, Unlimited)
from codenames.core.test_data import TestData


def convert_to_pb(dict_data: DictData) -> TestData:
    if 'agents' in dict_data:
        dict_agents = dict_data['agents']
        all_codenames = _get_all_codenames(dict_agents)
        secret_information = _get_secret_information(dict_agents)
        common_information = _get_common_information(dict_agents, all_codenames)
    else:
        all_codenames: Optional[set[Codename]] = None
        secret_information: SecretInformation = {}
        common_information: CommonInformation = {}
    if 'clues' in dict_data:
        dict_clues = dict_data['clues']
        clues = _get_team_clue_dict(dict_clues)
        shared_clues = _get_team_shared_clue_dict(clues)
    else:
        clues: TeamClueDict = {}
        shared_clues: TeamSharedClueDict = {}
    return TestData(secret_information, common_information, clues, shared_clues,
                    {}, {})


def _get_secret_information(agents: AgentDict) -> SecretInformation:
    secret_information = SecretInformation()
    for team, codenames in agents.items():
        secret_information.agent_sets[team].names.extend(codenames)
    return secret_information


def _get_common_information(agents: AgentDict,
                            all_codenames: set[Codename]) -> CommonInformation:
    common_information = CommonInformation()
    for team, codenames in agents.items():
        common_information.identity_counts[team] = len(codenames)
    all_codenames = sorted(list(all_codenames))
    common_information.agent_sets[UnknownTeam].names.extend(all_codenames)


def _get_all_codenames(agents: AgentDict) -> list[Codename]:
    all_codenames = set()
    for team_codenames in agents.values():
        team_codenames = set(team_codenames)
        if not all_codenames.isdisjoint(team_codenames):
            raise ValueError('codenames must be unique')
        all_codenames |= team_codenames
    return all_codenames


def _get_team_clue_dict(clues: TeamDictClueDict) -> TeamClueDict:
    return {
        team: [
            Clue(word=clue['word'], unlimited=True) if clue['quantity']
            == Unlimited else Clue(word=clue['word'], number=clue['quantity'])
            for clue in team_clues
        ] for team, team_clues in clues.items()
    }


def _get_team_shared_clue_dict(clues: TeamClueDict) -> TeamSharedClueDict:
    return {
        team: [SharedClue(team=team, clue=clue) for clue in team_clues
              ] for team, team_clues in clues.items()
    }