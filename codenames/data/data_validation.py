from typing import Optional

from codenames.data.types import (AssassinTeam, Codename, DictClue, NeutralTeam,
                                  Pass, StrAction, Team, UnknownTeam, Unlimited)


def validate_teams(teams: set[Team]) -> bool:
    n_teams = max(teams) + 1
    player_teams = set(range(n_teams))
    all_teams = player_teams | set((UnknownTeam, NeutralTeam, AssassinTeam))
    return teams.issuperset(player_teams) and teams.issubset(all_teams)


def validate_team(team: Team, n_teams: int = 2) -> bool:
    return isinstance(team, int) and -3 <= team < n_teams


def validate_codename(codename: Codename) -> bool:
    return isinstance(codename, str)


def validate_clue(clue: DictClue,
                  codenames: Optional[set[Codename]] = None) -> bool:
    if 'word' not in clue:
        return False
    if codenames is not None and clue['word'] in codenames:
        return False
    if 'quantity' not in clue:
        return False
    if not isinstance(clue['quantity'], int):
        return False
    if not (clue['quantity'] >= 1 or clue['quantity'] == Unlimited):
        return False
    return True


def validate_action(action: StrAction,
                    codenames: Optional[set[Codename]]) -> bool:
    if not isinstance(action, str):
        return False
    if codenames and not (action in codenames or action == Pass):
        return False
    return True