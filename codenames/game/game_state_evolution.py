from codenames.data.codenames_pb2 import Action, Clue, Role
from codenames.data.types import (
    AssassinTeam, Codename, EndTurn, NonPlayerTeams, Quantity, Team, Unlimited
)
from codenames.game.game_state import GameState
from codenames.game.game_validation import validate_action, validate_clue


def resolve_clue(game_state: GameState, clue: Clue) -> None:
    if not validate_clue(game_state, clue):
        raise ValueError
    game_state.guesses_remaining = Quantity(clue.quantity)
    game_state.active_role = Role.INTERPRETER


def resolve_action(game_state: GameState, action: Action) -> None:
    if not validate_action(action):
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
    game_state.team_outcomes.found_agents.append(team)


def _resolve_assassin(game_state: GameState) -> None:
    game_state.team_outcomes.found_assassin.append(game_state.teams.active_team)


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
