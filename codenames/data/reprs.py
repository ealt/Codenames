from typing import Any, Callable, Iterable, Mapping

from codenames.data.codenames_pb2 import Action
from codenames.data.codenames_pb2 import ActionOutcome
from codenames.data.codenames_pb2 import AgentSet
from codenames.data.codenames_pb2 import Clue
from codenames.data.codenames_pb2 import PlayerType
from codenames.data.codenames_pb2 import Role
from codenames.data.codenames_pb2 import SecretInformation
from codenames.data.codenames_pb2 import SharedAction
from codenames.data.codenames_pb2 import SharedClue
from codenames.data.types import AssassinTeam
from codenames.data.types import EndTurn
from codenames.data.types import NeutralTeam
from codenames.data.types import NullTeam
from codenames.data.types import UnknownTeam
from codenames.data.types import Unlimited


def snake_to_pascal(s: str) -> str:
    return s.replace('_', ' ').title().replace(' ', '')


def snake_to_camel(s: str) -> str:
    pascal = snake_to_pascal(s)
    return pascal[0].lower() + pascal[1:]


def iterable_repr(it: Iterable) -> str:
    return '[' + ', '.join(sorted(it)) + ']'


def mapping_repr(
    m: Mapping, key_func: Callable[[Any], str], val_func: Callable[[Any], str]
) -> str:
    return '{' + ', '.join([
        f'{key_func(k)}: {val_func(v)}'
        for k, v in sorted(m.items(), key=lambda item: item[0])
    ]) + '}'


def enum_name_repr(name: str) -> str:
    return name.lower().replace('_', ' ')


def identity_repr(identity: int) -> str:
    if identity == NullTeam:
        return 'null team'
    if identity == NeutralTeam:
        return 'neutral'
    if identity == AssassinTeam:
        return 'assassin'
    if identity == UnknownTeam:
        return 'unknown'
    return str(identity)


def role_repr(role: int) -> str:
    return enum_name_repr(Role.Name(role))  # type: ignore


def player_type_repr(player_type: PlayerType) -> str:
    return f'{player_type.team} {role_repr(player_type.role)}'


def agent_set_repr(agent_set: AgentSet) -> str:
    return iterable_repr(agent_set.codenames)


def secret_information_repr(secret_information: SecretInformation) -> str:
    return mapping_repr(
        secret_information.agent_sets, identity_repr, agent_set_repr
    )


def clue_repr(clue: Clue) -> str:
    quantity = 'unlimited' if clue.quantity == Unlimited else clue.quantity
    return f'{{word: {clue.word}, quantity: {quantity}}}'


def shared_clue_repr(shared_clue: SharedClue) -> str:
    return f'{{team: {shared_clue.team}, clue: {clue_repr(shared_clue.clue)}}}'


def action_repr(action: Action) -> str:
    return 'end turn' if action.guess == EndTurn else action.guess


def action_outcome_repr(action_outcome: ActionOutcome) -> str:
    return identity_repr(action_outcome.identity)


def shared_action_repr(shared_action: SharedAction) -> str:
    return (
        f'{{team: {shared_action.team}, '
        f'action: {action_repr(shared_action.action)}, '
        f'outcome: {action_outcome_repr(shared_action.action_outcome)}}}'
    )
