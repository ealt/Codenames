from typing import Iterator

from codenames.data.types import NullTeam
from codenames.data.types import Team
from codenames.game.player_team import PlayerTeam


class PlayerTeams:

    def __init__(self, teams: list[Team]) -> None:
        self.__len = len(teams)
        self._active = PlayerTeam(NullTeam)
        if teams:
            self._init_cyclic_doubly_linked_list(teams)

    def _init_cyclic_doubly_linked_list(self, teams: list[Team]) -> None:
        if not teams:
            return
        player_teams = [PlayerTeam(team) for team in teams]
        prev = player_teams[-1]
        for player_team in player_teams:
            curr = player_team
            prev.next = curr
            curr.prev = prev
            prev = curr
        self._active = prev.next

    @property
    def active_team(self) -> Team:
        return self._active.team

    def __len__(self) -> int:
        return self.__len

    def __getitem__(self, team: Team) -> PlayerTeam:
        curr = self._active
        while curr.team != team:
            curr = curr.next
            if curr == self._active:
                raise KeyError
        return curr

    def __delitem__(self, team: Team) -> None:
        node = self[team]
        node.prev.next = node.next
        node.next.prev = node.prev
        self.__len -= 1
        if len(self) == 0:
            self._active = PlayerTeam(NullTeam)
        elif node == self._active:
            self._active = node.next

    def __iter__(self) -> Iterator[Team]:
        return self

    def __next__(self) -> Team:
        self._active = self._active.next
        return self._active.prev.team

    def __contains__(self, team: Team) -> bool:
        try:
            _ = self[team]
        except KeyError:
            return False
        return True
