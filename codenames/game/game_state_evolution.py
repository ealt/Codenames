from codenames.data.codenames_pb2 import Action, Clue, Role
from codenames.data.types import (
    AssassinTeam, Codename, EndTurn, NonPlayerTeams, Quantity, Team, Unlimited
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
        if (not game_state.unknown_agents[identity]
                and identity not in NonPlayerTeams):
            _resolve_found_agents(game_state, identity)
            _end_turn(game_state)
        elif identity == game_state.teams.active_team:
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


def _resolve_found_agents(game_state: GameState, team: Team) -> None:
    pass


def _resolve_assassin(game_state: GameState) -> None:
    pass


def _end_turn(game_state: GameState) -> None:
    _ = next(game_state.teams)
    game_state.active_role = Role.CODEMASTER
    game_state.guesses_remaining = Quantity(0)
