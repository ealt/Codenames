from logging import Logger

from codenames.data.codenames_pb2 import Action
from codenames.data.codenames_pb2 import Clue
from codenames.data.codenames_pb2 import PlayerType
from codenames.data.codenames_pb2 import Role
from codenames.data.codenames_pb2 import SecretInformation
from codenames.data.codenames_pb2 import SharedAction
from codenames.data.codenames_pb2 import SharedClue
import codenames.data.reprs as rp
from codenames.data.types import Team
from codenames.logging.base_logger import BaseLogger
from codenames.players.team_players import TeamPlayers


class GameLogger(BaseLogger):

    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)

    def log_players(self, players: dict[Team, TeamPlayers]) -> None:
        for team, team_players in players.items():
            self.logger.info(
                f'{team} {rp.role_repr(Role.CLUE_GIVER)}: '
                f'{team_players.clue_giver.__class__.__name__}'
            )
            self.logger.info(
                f'{team} {rp.role_repr(Role.GUESSER)}: '
                f'{team_players.guesser.__class__.__name__}'
            )

    def log_secret_information(
        self, secret_information: SecretInformation
    ) -> None:
        self.logger.info(
            f'Secret information: '
            f'{rp.secret_information_repr(secret_information)}'  # type: ignore
        )

    def log_active_player(self, team: Team, role: int) -> None:
        self.logger.debug(f'Active player: {team} {rp.role_repr(role)}')

    def log_invalid_role(self, role: int) -> None:
        if role in Role.values():
            self.logger.error(
                f'Invalid role: {rp.role_repr(role)} '  # type: ignore
                'for active player'
            )
        else:
            self.logger.error(f'Unknown role: {role!r} for active player')

    def log_clue(self, clue: Clue) -> None:
        self.logger.debug(f'Clue given: {rp.clue_repr(clue)}')

    def log_invalid_clue_word(self, word: str) -> None:
        self.logger.error(f'Invalid clue word: {word}')

    def log_invalid_clue_number(self, number: int) -> None:
        self.logger.error(f'Invalid clue number: {number}')

    def log_invalid_clue_quantity(self) -> None:
        self.logger.error('Invalid clue quantity')

    def log_shared_clue(self, shared_clue: SharedClue) -> None:
        self.logger.info(f'Shared clue: {rp.shared_clue_repr(shared_clue)}')

    def log_action(self, action: Action) -> None:
        self.logger.debug(f'Action given: {rp.action_repr(action)}')

    def log_invalid_guess(self, guess: str) -> None:
        self.logger.error(f'Invalid guess: {guess}')

    def log_invalid_action(self) -> None:
        self.logger.error('Invalid action')

    def log_incorrect_guess(self) -> None:
        self.logger.debug('The guesser identified an agent')

    def log_exhausted_guesses(self) -> None:
        self.logger.debug('The guesser used all their guesses')

    def log_pass(self) -> None:
        self.logger.debug('The guesser ended their turn')

    def log_shared_action(self, shared_action: SharedAction) -> None:
        self.logger.info(
            f'Shared action: {rp.shared_action_repr(shared_action)}'
        )

    def log_end_turn(self, player_type: PlayerType) -> None:
        self.logger.debug(f'End of turn for player: {player_type}')
