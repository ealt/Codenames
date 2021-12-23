from codenames.data.types import NonPlayerTeams, Team


def validate_teams(teams: set[Team]) -> bool:
    n_teams = max(teams)
    player_teams = set(range(1, n_teams + 1))
    all_teams = player_teams | NonPlayerTeams
    return teams.issuperset(player_teams) and teams.issubset(all_teams)
