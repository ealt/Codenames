from typing import Optional

from codenames.data.codenames_pb2 import Role, SecretInformation
from codenames.data.types import (
    CodenameIdentities, IdentityCodenames, NonPlayerTeams, Quantity, Team,
    TeamOutcomes
)
from codenames.game.game_state import GameState
from codenames.game.player_teams import PlayerTeams


def get_game_state(
    secret_information: SecretInformation,
    ordered_teams: Optional[list[Team]] = None
) -> GameState:
    if ordered_teams is None:
        ordered_teams = _get_ordered_teams(secret_information)
    codename_identities = get_codename_identities(secret_information)
    unknown_agents = _get_unknown_agents(secret_information)
    teams = PlayerTeams(ordered_teams)
    team_outcomes = _get_team_outcomes(ordered_teams, unknown_agents)
    active_role = Role.CODEMASTER
    guesses_remaining = Quantity(0)
    return GameState(
        codename_identities,
        unknown_agents,
        teams,
        team_outcomes,
        active_role,
        guesses_remaining,
    )


def _get_ordered_teams(secret_information: SecretInformation) -> list[Team]:
    all_teams = set(secret_information.agent_sets.keys())
    player_teams = all_teams - NonPlayerTeams
    return sorted(list(player_teams))


def get_codename_identities(
    secret_information: SecretInformation
) -> CodenameIdentities:
    return {
        codename: team
        for team, agent_set in secret_information.agent_sets.items()
        for codename in agent_set.codenames
    }


def _get_unknown_agents(
    secret_information: SecretInformation
) -> IdentityCodenames:
    return IdentityCodenames({
        Team(team): set(agent_set.codenames)
        for team, agent_set in secret_information.agent_sets
    })


def _get_team_outcomes(
    teams: list[Team], unknown_agents: IdentityCodenames
) -> TeamOutcomes:
    found_agents = [team for team in teams if not unknown_agents[team]]
    return TeamOutcomes(found_agents=found_agents)
