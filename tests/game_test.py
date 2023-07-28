from collections import defaultdict
import json
from pathlib import Path
from typing import cast

import pytest

from codenames.data.codenames_pb2 import Action
from codenames.data.codenames_pb2 import Clue
from codenames.data.codenames_pb2 import SecretInformation
from codenames.data.types import NonPlayerTeams
from codenames.data.types import Quantity
from codenames.data.types import Team
from codenames.data.types import TeamOutcomes
from codenames.game.game import Game
import codenames.game.game_state_generation as gsg
from codenames.logging.game_logger import GameLogger
from codenames.logging.logger_factory import CodeTalkerLoggerFactory
from codenames.logging.types import LoggingData
from codenames.players.team_players import TeamPlayers
from tests.data.types import Actions as JsonActions
from tests.data.types import Clue as JsonClue
from tests.data.types import IdentityCodenames as JsonIdentityCodenames
from tests.data.types import TeamOutcomes as JsonTeamOutcomes
from tests.data.types import TestData
from tests.data.types import TurnHistory as JsonTurnHistory
from tests.preprogrammed_codemaster import PreprogrammedCodemaster
from tests.preprogrammed_interpreter import PreprogrammedInterpreter

game_names = [
    'found_agents',
    'found_assassin',
    'pass',
    'fumble',
    'guess_limit',
]


@pytest.mark.parametrize('game_name', game_names, ids=game_names)
def test_game(game_name: str) -> None:
    test_data = _load_test_data(game_name)
    identity_codenames = cast(
        JsonIdentityCodenames, test_data['identity_codenames']
    )
    player_teams = _get_player_teams(identity_codenames)
    turn_history = cast(JsonTurnHistory, test_data['turn_history'])
    players = _get_players(player_teams, turn_history)
    secret_information = _get_secret_information(identity_codenames)
    game_state = gsg.get_game_state(secret_information, player_teams)
    logging_data = _get_logging_data(game_name)
    logger_factory = CodeTalkerLoggerFactory(logging_data)
    game_logger = logger_factory.get_logger(GameLogger)
    game = Game(players, game_state, game_logger)
    game.play()
    team_outcomes = cast(JsonTeamOutcomes, test_data['team_outcomes'])
    expected_outcomes = _get_team_outcomes(team_outcomes)
    assert game.game_state.team_outcomes == expected_outcomes


def _load_test_data(game_name: str) -> TestData:
    current_dir = Path(__file__).resolve().parent
    data_path = current_dir / 'data' / f'{game_name}.json'
    with open(data_path) as f:
        test_data: TestData = json.loads(f.read())
    return test_data


def _get_player_teams(identity_codenames: JsonIdentityCodenames) -> list[Team]:
    return [
        team for team in map(lambda k: Team(int(k)), identity_codenames.keys())
        if team not in NonPlayerTeams
    ]


def _get_players(player_teams: list[Team],
                 turn_history: JsonTurnHistory) -> dict[Team, TeamPlayers]:
    clues = _get_clues(turn_history)
    actions = _get_actions(turn_history)
    return {
        team:
            TeamPlayers(
                codemaster=PreprogrammedCodemaster(clues[team]),
                interpreter=PreprogrammedInterpreter(actions[team])
            )
        for team in player_teams
    }


def _get_clues(turn_history: JsonTurnHistory) -> dict[Team, list[Clue]]:
    clues: dict[Team, list[Clue]] = defaultdict(list)
    for turn in turn_history:
        team = Team(cast(int, turn['team']))
        clue = cast(JsonClue, turn['clue'])
        clues[team].append(
            Clue(
                word=cast(str, clue['word']),
                quantity=Quantity(cast(int, clue['quantity']))
            )
        )
    return clues


def _get_actions(turn_history: JsonTurnHistory) -> dict[Team, list[Action]]:
    actions: dict[Team, list[Action]] = defaultdict(list)
    for turn in turn_history:
        team = Team(cast(int, turn['team']))
        actions[team].extend(
            list(
                map(
                    lambda action: Action(guess=action),
                    cast(JsonActions, turn['actions'])
                )
            )
        )
    return actions


def _get_secret_information(
    identity_codenames: JsonIdentityCodenames
) -> SecretInformation:
    secret_information = SecretInformation()
    for identity, codenames in identity_codenames.items():
        team = int(identity)
        secret_information.agent_sets[team].codenames.extend(codenames)
    return secret_information


def _get_logging_data(game_name: str) -> LoggingData:
    return {
        'path': Path(__file__).resolve().parent / 'logs',
        'config_mods': {
            'game': {
                'filename': f'{game_name}_game.log',
                'level': 'DEBUG',
                'mode': 'w',
            },
        }
    }


def _get_team_outcomes(team_outcomes: JsonTeamOutcomes) -> TeamOutcomes:
    return TeamOutcomes(
        found_agents=list(map(Team, team_outcomes['found_agents'])),
        found_assassin=list(map(Team, team_outcomes['found_assassin']))
    )
