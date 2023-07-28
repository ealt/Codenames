from codenames.data.types import NullTeam
from codenames.data.types import Team
from codenames.game.player_team_list import PlayerTeamList


def test_layer_teams_len() -> None:
    player_teams = PlayerTeamList([Team(1), Team(2), Team(3), Team(4)])
    assert len(player_teams) == 4


def test_player_teams_contains() -> None:
    player_teams = PlayerTeamList([Team(1), Team(2), Team(4)])
    assert Team(2) in player_teams
    assert Team(3) not in player_teams


def test_player_teams_del() -> None:
    player_teams = PlayerTeamList([Team(1), Team(2), Team(3), Team(4)])
    assert Team(3) in player_teams
    del player_teams[Team(3)]
    assert Team(3) not in player_teams


def test_player_teams_iter() -> None:
    player_teams = PlayerTeamList([Team(1), Team(2), Team(4)])
    assert next(player_teams) == Team(1)
    expected_teams = [Team(2), Team(4), Team(1), Team(2), Team(4), Team(1)]
    for actual, expected in zip(player_teams, expected_teams):
        assert actual == expected


def test_player_teams_del_iter() -> None:
    player_teams = PlayerTeamList([Team(1), Team(2), Team(3), Team(4)])
    # 1 -> 2 -> 3 -> 4 -> ...
    assert next(player_teams) == Team(1)
    # 2 -> 3 -> 4 -> 1 -> ...
    assert player_teams.active_team == Team(2)
    del player_teams[Team(2)]
    # 3 -> 4 -> 1 -> ...
    assert player_teams.active_team == Team(3)
    del player_teams[Team(4)]
    # 3 -> 1 -> ...
    assert next(player_teams) == Team(3)
    # 1 -> 3 -> ...
    del player_teams[Team(3)]
    # 1 -> ...
    del player_teams[Team(1)]
    # [None]
    assert player_teams.active_team == NullTeam
