from codenames.data.types import Team


class PlayerTeamNode:

    def __init__(self, team: Team) -> None:
        self._team = team
        self.prev: PlayerTeamNode = self
        self.next: PlayerTeamNode = self

    @property
    def team(self) -> Team:
        return self._team
