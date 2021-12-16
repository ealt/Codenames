from collections import defaultdict

from codenames.data.codenames_pb2 import (
    Action, Clue, CommonInformation, SecretInformation, SharedAction, SharedClue
)
from codenames.data.data_validation import (
    validate_action, validate_clue, validate_codename, validate_team
)
from codenames.data.test_data import TestData
from codenames.data.types import (
    AgentDict, Codename, CodenameIdentities, DictData, EndTurn, TeamActionDict,
    TeamClueDict, TeamDictClueDict, TeamSharedActionDict, TeamSharedClueDict,
    TeamStrActionDict, UnknownTeam
)


def convert_to_pb(dict_data: DictData) -> TestData:
    codenames: set[Codename] = set()
    codename_identities = CodenameIdentities({})
    secret_information = SecretInformation()
    common_information = CommonInformation()
    clues = TeamClueDict({})
    shared_clues = TeamSharedClueDict({})
    actions = TeamActionDict({})
    shared_actions = TeamSharedActionDict({})
    if 'agents' in dict_data:
        dict_agents = dict_data['agents']
        valid_agents = _get_valid_agents(dict_agents)
        codenames = _get_codenames(valid_agents)
        codename_identities = _get_codename_identities(valid_agents)
        secret_information = _get_secret_information(valid_agents)
        common_information = _get_common_information(valid_agents, codenames)
    if 'clues' in dict_data:
        dict_clues = dict_data['clues']
        valid_clues = _get_valid_clues(dict_clues, codenames)
        clues = _get_team_clue_dict(valid_clues)
        shared_clues = _get_team_shared_clue_dict(clues)
    if 'actions' in dict_data:
        dict_actions = dict_data['actions']
        valid_actions = _get_valid_actions(dict_actions, codenames)
        actions = _get_team_action_dict(valid_actions)
        shared_actions = _get_team_shared_action_dict(
            actions, codename_identities
        )
    return TestData(
        secret_information,
        common_information,
        clues,
        shared_clues,
        actions,
        shared_actions,
    )


def _get_valid_agents(agents: AgentDict) -> AgentDict:
    return {
        team: sorted([
            codename for codename in set(codenames)
            if validate_codename(codename)
        ])
        for team, codenames in agents.items()
        if validate_team(team)
    }


def _get_secret_information(agents: AgentDict) -> SecretInformation:
    secret_information = SecretInformation()
    for team, codenames in agents.items():
        secret_information.agent_sets[team].codenames.extend(codenames)
    return secret_information


def _get_common_information(
    agents: AgentDict, codenames: set[Codename]
) -> CommonInformation:
    common_information = CommonInformation()
    for team, team_codenames in agents.items():
        common_information.identity_counts[team] = len(team_codenames)
    sorted_codenames = sorted(list(codenames))
    common_information.agent_sets[UnknownTeam].codenames.extend(
        sorted_codenames
    )
    return common_information


def _get_codenames(agents: AgentDict) -> set[Codename]:
    codenames: set[Codename] = set()
    for team_codenames in agents.values():
        team_codename_set = set(team_codenames)
        if not codenames.isdisjoint(team_codename_set):
            raise ValueError('codenames must be unique')
        codenames |= team_codename_set
    return codenames


def _get_codename_identities(agents: AgentDict) -> CodenameIdentities:
    return {
        codename: team
        for team, codenames in agents.items() for codename in codenames
    }


def _get_valid_clues(
    clues: TeamDictClueDict, codenames: set[Codename]
) -> TeamDictClueDict:
    return TeamDictClueDict({
        team: [clue for clue in team_clues if validate_clue(clue, codenames)]
        for team, team_clues in clues.items()
        if validate_team(team)
    })


def _get_team_clue_dict(clues: TeamDictClueDict) -> TeamClueDict:
    return TeamClueDict({
        team: [
            Clue(word=clue['word'], quantity=clue['quantity'])
            for clue in team_clues
        ]
        for team, team_clues in clues.items()
    })


def _get_team_shared_clue_dict(clues: TeamClueDict) -> TeamSharedClueDict:
    return TeamSharedClueDict({
        team: [SharedClue(team=team, clue=clue) for clue in team_clues]
        for team, team_clues in clues.items()
    })


def _get_valid_actions(
    actions: TeamStrActionDict, codenames: set[Codename]
) -> TeamStrActionDict:
    return TeamStrActionDict({
        team: [
            action for action in team_actions
            if validate_action(action, codenames)
        ]
        for team, team_actions in actions.items()
        if validate_team(team)
    })


def _get_team_action_dict(actions: TeamStrActionDict) -> TeamActionDict:
    return TeamActionDict({
        team: [Action(guess=action) for action in team_actions]
        for team, team_actions in actions.items()
    })


def _get_team_shared_action_dict(
    actions: TeamActionDict, agent_identities: CodenameIdentities
) -> TeamSharedActionDict:
    shared_actions = TeamSharedActionDict(defaultdict(list))
    for team, team_actions in actions.items():
        for action in team_actions:
            shared_action = SharedAction(team=team, action=action)
            if action.guess != EndTurn:
                identity = agent_identities.get(action.guess, UnknownTeam)
                shared_action.action_outcome.identity = identity
            shared_actions[team].append(shared_action)
    return shared_actions
