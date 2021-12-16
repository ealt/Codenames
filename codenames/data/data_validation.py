from codenames.data.types import (
    Codename, DictClue, NonPlayerTeams, EndTurn, StrAction, Team, Unlimited
)


def validate_teams(teams: set[Team]) -> bool:
    n_teams = max(teams)
    player_teams = set(range(1, n_teams + 1))
    all_teams = player_teams | NonPlayerTeams
    return teams.issuperset(player_teams) and teams.issubset(all_teams)


def validate_team(team: Team, n_teams: int = 2) -> bool:
    return (
        isinstance(team, int)
        and (0 < team <= n_teams or team in NonPlayerTeams)
    )


def validate_codename(codename: Codename) -> bool:
    return isinstance(codename, str)


def validate_clue(clue: DictClue, codenames: set[Codename]) -> bool:
    if 'word' not in clue:
        return False
    if clue['word'] in codenames:
        return False
    if 'quantity' not in clue:
        return False
    if not isinstance(clue['quantity'], int):
        return False
    if not (clue['quantity'] >= 1 or clue['quantity'] == Unlimited):
        return False
    return True


def validate_action(action: StrAction, codenames: set[Codename]) -> bool:
    if not isinstance(action, str):
        return False
    if codenames and not (action in codenames or action == EndTurn):
        return False
    return True
