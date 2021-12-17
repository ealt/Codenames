from codenames.data.types import NullTeam, Team
from codenames.game.player_team import PlayerTeam


class PlayerTeams:

    def __init__(self, teams: list[Team]) -> None:
        self._active = PlayerTeam(NullTeam)
        if teams:
            self._init_cyclic_doubly_linked_list(teams)

    def _init_cyclic_doubly_linked_list(self, teams: list[Team]) -> None:
        self._active = PlayerTeam(teams[0])
        prev = self._active
        for team in teams[1:]:
            curr = PlayerTeam(team)
            prev.next = curr
            curr.prev = prev
            prev = curr
        curr.next = self._active
        self._active.prev = curr

    @property
    def active_team(self) -> Team:
        return self._active.team
