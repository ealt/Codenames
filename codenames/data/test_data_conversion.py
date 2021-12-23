from collections import defaultdict

from codenames.data.codenames_pb2 import (
    CommonInformation, SecretInformation, SharedAction, Turn
)
from codenames.data.data_validation import (
    validate_action, validate_clue, validate_codename, validate_team
)
from codenames.data.test_data import TestData
from codenames.data.types import (
    AgentDict, Codename, CodenameIdentities, DictData, DictTurn, EndTurn,
    NullTeam, TeamActionDict, TeamClueDict, UnknownTeam
)


def convert_to_pb(dict_data: DictData) -> TestData:
    codenames: set[Codename] = set()
    codename_identities = CodenameIdentities({})
    secret_information = SecretInformation()
    common_information = CommonInformation()
    clues = TeamClueDict({})
    actions = TeamActionDict({})
    if 'agents' in dict_data:
        dict_agents = dict_data['agents']
        valid_agents = _get_valid_agents(dict_agents)
        codenames = _get_codenames(valid_agents)
        codename_identities = _get_codename_identities(valid_agents)
        secret_information = _get_secret_information(valid_agents)
        common_information = _get_common_information(valid_agents, codenames)
    if 'turns' in dict_data:
        turns = dict_data['turns']
        _update_common_information(
            common_information, turns, codenames, codename_identities
        )
        clues = _get_team_clue_dict(common_information)
        actions = _get_team_action_dict(common_information)
    return TestData(
        secret_information,
        common_information,
        clues,
        actions,
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


def _update_common_information(
    common_information: CommonInformation,
    turns: list[DictTurn],
    codenames: set[Codename],
    codename_identities: CodenameIdentities,
) -> None:
    for dict_turn in turns:
        team = dict_turn['team']
        dict_clue = dict_turn['clue']
        if validate_team(team) and validate_clue(dict_clue, codenames):
            turn = _get_turn(
                codenames, codename_identities, dict_turn, team, dict_clue
            )
            common_information.turn_history.append(turn)


def _get_turn(codenames, codename_identities, dict_turn, team, dict_clue):
    turn = Turn()
    turn.clue.team = team
    turn.clue.clue.word = dict_clue['word']
    turn.clue.clue.quantity = dict_clue['quantity']
    for str_action in dict_turn['actions']:
        if validate_action(str_action, codenames):
            action = _get_action(codename_identities, team, str_action)
            turn.actions.append(action)
    return turn


def _get_action(codename_identities, team, str_action):
    if str_action == EndTurn:
        identity = NullTeam
    else:
        identity = codename_identities.get(str_action, UnknownTeam)
    action = SharedAction()
    action.team = team
    action.action.guess = str_action
    action.action_outcome.identity = identity
    return action


def _get_team_clue_dict(common_information: CommonInformation) -> TeamClueDict:
    team_clue_dict = TeamClueDict(defaultdict(list))
    for turn in common_information.turn_history:
        team_clue_dict[turn.clue.team].append(turn.clue.clue)
    return team_clue_dict


def _get_team_action_dict(
    common_information: CommonInformation
) -> TeamActionDict:
    team_action_dict = TeamActionDict(defaultdict(list))
    for turn in common_information.turn_history:
        for action in turn.actions:
            team_action_dict[action.team].append(action.action)
    return team_action_dict
