from codenames.data.types import Team


class PlayerTeam:

    def __init__(self, team: Team) -> None:
        self._team = team
        self.prev: PlayerTeam = self
        self.next: PlayerTeam = self

    @property
    def team(self) -> Team:
        return self._team
