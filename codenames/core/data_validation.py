from codenames.core.types import Codename, Team


def validate_team(team: Team, num_teams: int = 2) -> bool:
    return isinstance(team, int) and -1 <= team <= num_teams


def validate_codename(codename: Codename) -> bool:
    return isinstance(codename, str)