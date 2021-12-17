from codenames.data.codenames_pb2 import Action, Clue, Role
from codenames.data.types import (
    AssassinTeam, Codename, EndTurn, Quantity, Team, Unlimited
)
from codenames.game.game_state import GameState


def resolve_clue(game_state: GameState, clue: Clue) -> None:
    game_state.guesses_remaining = Quantity(clue.quantity)
    game_state.active_role = Role.INTERPRETER


def resolve_action(game_state: GameState, action: Action) -> None:
    if action.guess == EndTurn:
        _end_turn(game_state)
    else:
        codename = Codename(action.guess)
        identity = game_state.codename_identities[codename]
        game_state.unknown_agents[identity].remove(codename)
        if identity == game_state.active_team:
            if game_state.guesses_remaining != Unlimited:
                game_state.guesses_remaining = Quantity(
                    game_state.guesses_remaining - 1
                )
            if game_state.guesses_remaining == Quantity(0):
                _end_turn(game_state)
        else:
            if identity == AssassinTeam:
                _resolve_assassin(game_state)
            _end_turn(game_state)


def _resolve_assassin(game_state: GameState) -> None:
    pass


def _end_turn(game_state: GameState) -> None:
    game_state.active_team = _get_next_team(game_state)
    game_state.active_role = Role.CODEMASTER
    game_state.guesses_remaining = Quantity(0)


def _get_next_team(game_state: GameState) -> Team:
    teams = game_state.team_outcomes.undetermined
    n_teams = len(teams)
    current_index = teams.index(game_state.active_team)
    next_index = (current_index + 1) % n_teams
    return Team(teams(next_index))
