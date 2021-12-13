from collections import defaultdict
from typing import Optional

from codenames.data.codenames_pb2 import (Action, Clue, CommonInformation,
                                          SecretInformation, SharedAction,
                                          SharedClue)
from codenames.data.data_validation import (validate_action, validate_clue,
                                            validate_codename, validate_team)
from codenames.data.test_data import TestData
from codenames.data.types import (AgentDict, AgentIdentities, Codename,
                                  DictData, Pass, TeamActionDict, TeamClueDict,
                                  TeamDictClueDict, TeamSharedActionDict,
                                  TeamSharedClueDict, TeamStrActionDict,
                                  UnknownTeam)


def convert_to_pb(dict_data: DictData) -> TestData:
    if 'agents' in dict_data:
        dict_agents = dict_data['agents']
        valid_agents = _get_valid_agents(dict_agents)
        all_codenames = _get_all_codenames(valid_agents)
        agent_identities = _get_agent_identities(valid_agents)
        secret_information = _get_secret_information(valid_agents)
        common_information = _get_common_information(valid_agents,
                                                     all_codenames)
    else:
        all_codenames: Optional[set[Codename]] = None
        agent_identities: AgentIdentities = {}
        secret_information: SecretInformation = {}
        common_information: CommonInformation = {}
    if 'clues' in dict_data:
        dict_clues = dict_data['clues']
        valid_clues = _get_valid_clues(dict_clues, all_codenames)
        clues = _get_team_clue_dict(valid_clues)
        shared_clues = _get_team_shared_clue_dict(clues)
    else:
        clues: TeamClueDict = {}
        shared_clues: TeamSharedClueDict = {}
    if 'actions' in dict_data:
        dict_actions = dict_data['actions']
        valid_actions = _get_valid_actions(dict_actions, all_codenames)
        actions = _get_team_action_dict(valid_actions)
        shared_actions = _get_team_shared_action_dict(actions, agent_identities)
    else:
        actions: TeamActionDict = {}
        shared_actions: TeamSharedActionDict = {}
    return TestData(secret_information, common_information, clues, shared_clues,
                    actions, shared_actions)


def _get_valid_agents(agents: AgentDict) -> AgentDict:
    return {
        team: sorted([
            codename for codename in set(codenames)
            if validate_codename(codename)
        ]) for team, codenames in agents.items() if validate_team(team)
    }


def _get_secret_information(agents: AgentDict) -> SecretInformation:
    secret_information = SecretInformation()
    for team, codenames in agents.items():
        secret_information.agent_sets[team].codenames.extend(codenames)
    return secret_information


def _get_common_information(agents: AgentDict,
                            all_codenames: set[Codename]) -> CommonInformation:
    common_information = CommonInformation()
    for team, codenames in agents.items():
        common_information.identity_counts[team] = len(codenames)
    all_codenames = sorted(list(all_codenames))
    common_information.agent_sets[UnknownTeam].codenames.extend(all_codenames)
    return common_information


def _get_all_codenames(agents: AgentDict) -> list[Codename]:
    all_codenames = set()
    for team_codenames in agents.values():
        team_codenames = set(team_codenames)
        if not all_codenames.isdisjoint(team_codenames):
            raise ValueError('codenames must be unique')
        all_codenames |= team_codenames
    return all_codenames


def _get_agent_identities(agents: AgentDict) -> AgentIdentities:
    return {
        codename: team for team, codenames in agents.items()
        for codename in codenames
    }


def _get_valid_clues(clues: TeamDictClueDict,
                     all_codenames: set[Codename]) -> TeamDictClueDict:
    return {
        team:
        [clue for clue in team_clues if validate_clue(clue, all_codenames)]
        for team, team_clues in clues.items()
        if validate_team(team)
    }


def _get_team_clue_dict(clues: TeamDictClueDict) -> TeamClueDict:
    return {
        team: [
            Clue(word=clue['word'], quantity=clue['quantity'])
            for clue in team_clues
        ] for team, team_clues in clues.items()
    }


def _get_team_shared_clue_dict(clues: TeamClueDict) -> TeamSharedClueDict:
    return {
        team: [SharedClue(team=team, clue=clue) for clue in team_clues
              ] for team, team_clues in clues.items()
    }


def _get_valid_actions(actions: TeamStrActionDict,
                       all_codenames: set[Codename]) -> TeamStrActionDict:
    return {
        team: [
            action for action in team_actions
            if validate_action(action, all_codenames)
        ] for team, team_actions in actions.items() if validate_team(team)
    }


def _get_team_action_dict(actions: TeamStrActionDict) -> TeamActionDict:
    return {
        team: [Action(guess=action) for action in team_actions
              ] for team, team_actions in actions.items()
    }


def _get_team_shared_action_dict(
        actions: TeamActionDict,
        agent_identities: AgentIdentities) -> TeamSharedActionDict:
    shared_actions = defaultdict(list)
    for team, team_actions in actions.items():
        for action in team_actions:
            shared_action = SharedAction(team=team, action=action)
            if action.guess != Pass:
                identity = agent_identities.get(action.guess, UnknownTeam)
                shared_action.action_outcome.identity = identity
            shared_actions[team].append(shared_action)
    return shared_actions
