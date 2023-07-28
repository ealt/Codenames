from codenames.data.codenames_pb2 import Action
from codenames.data.codenames_pb2 import Clue
from codenames.data.codenames_pb2 import CommonInformation
from codenames.data.codenames_pb2 import Role
from codenames.data.types import AssassinTeam
from codenames.data.types import Codename
from codenames.data.types import EndTurn
from codenames.data.types import NonPlayerTeams
from codenames.data.types import Quantity
from codenames.data.types import Team
from codenames.data.types import Unlimited
from codenames.game.game_state import GameState
import codenames.game.game_validation as gv


def update_state(
    game_state: GameState, common_information: CommonInformation
) -> None:
    for turn in common_information.turn_history:
        resolve_clue(game_state, turn.clue.clue)
        for action in turn.actions:
            resolve_action(game_state, action.action)


def resolve_clue(game_state: GameState, clue: Clue) -> None:
    if not gv.validate_clue(game_state, clue):
        raise ValueError
    game_state.guesses_remaining = Quantity(clue.quantity)
    game_state.active_role = Role.INTERPRETER


def resolve_action(game_state: GameState, action: Action) -> None:
    if not gv.validate_action(game_state, action):
        raise ValueError
    if action.guess == EndTurn:
        _end_turn(game_state)
    else:
        guess = Codename(action.guess)
        _resolve_guess(game_state, guess)


def _resolve_guess(game_state: GameState, guess: Codename) -> None:
    identity = game_state.codename_identities[guess]
    game_state.unknown_agents[identity].remove(guess)
    if identity in NonPlayerTeams:
        _resolve_non_player_team_guess(game_state, identity)
    else:
        _resolve_player_team_guess(game_state, identity)


def _resolve_non_player_team_guess(
    game_state: GameState, identity: Team
) -> None:
    if identity == AssassinTeam:
        _resolve_assassin(game_state)
    _end_turn(game_state)


def _resolve_player_team_guess(game_state: GameState, identity: Team) -> None:
    if not game_state.unknown_agents[identity]:
        _resolve_found_agents(game_state, identity)
    if identity == game_state.teams.active_team:
        _resolve_successful_guess(game_state)
    else:
        _end_turn(game_state)


def _resolve_found_agents(game_state: GameState, team: Team) -> None:
    del game_state.teams[team]
    game_state.team_outcomes.found_agents.append(team)


def _resolve_assassin(game_state: GameState) -> None:
    team = game_state.teams.active_team
    del game_state.teams[team]
    game_state.team_outcomes.found_assassin.append(team)


def _resolve_successful_guess(game_state: GameState) -> None:
    if game_state.guesses_remaining != Unlimited:
        game_state.guesses_remaining = Quantity(
            game_state.guesses_remaining - 1
        )
    if game_state.guesses_remaining == Quantity(0):
        _end_turn(game_state)


def _end_turn(game_state: GameState) -> None:
    _ = next(game_state.teams)
    game_state.active_role = Role.CODEMASTER
    game_state.guesses_remaining = Quantity(0)
