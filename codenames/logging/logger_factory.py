import logging
import logging.config
from pathlib import Path
from typing import cast, Type

import yaml

import codenames.data.reprs as rp
from codenames.logging.base_logger import BaseLogger
from codenames.logging.game_logger import GameLogger
from codenames.logging.logger_type import LoggerType
from codenames.logging.types import ConfigMods
from codenames.logging.types import Logger
from codenames.logging.types import LoggingData


class CodeTalkerLoggerFactory:

    def __init__(self, data: LoggingData) -> None:
        logs_path = Path(__file__).resolve().parent.parent / 'logs'
        config_mods: ConfigMods = {}
        if data:
            if 'path' in data:
                logs_path = cast(Path, data['path'])
                logs_path = Path(logs_path).resolve()
            if 'config_mods' in data:
                config_mods = cast(ConfigMods, data['config_mods'])
        self._init_from_yaml(logs_path, config_mods)
        self._set_loggers()

    def get_logger(self, logger_type: Type[Logger]) -> Logger:
        return self._loggers[logger_type]  # type: ignore

    def _init_from_yaml(self, logs_path: Path, config_mods: ConfigMods) -> None:
        config_dir = Path(__file__).resolve().parent.parent.parent
        config_path = config_dir / 'logging.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f.read())
        self._update_config(config, logs_path, config_mods)
        logging.config.dictConfig(config)

    def _update_config(
        self, config, logs_path: Path, config_mods: ConfigMods
    ) -> None:
        for logger_type, config_mod in config_mods.items():
            if logger_type.upper() in LoggerType._member_names_:
                logger_type = rp.snake_to_camel(logger_type)
                logger_config = config['loggers'][logger_type]
                handler_name = f'{logger_type}FileHandler'
                handler_config = config['handlers'][handler_name]
                if 'filename' in config_mod:
                    filepath = logs_path / config_mod['filename']
                    handler_config['filename'] = filepath
                if 'level' in config_mod:
                    logger_config['level'] = config_mod['level']
                    handler_config['level'] = config_mod['level']
                if 'mode' in config_mod:
                    handler_config['mode'] = config_mod['mode']

    def _set_loggers(self) -> None:
        self._loggers = {
            GameLogger: GameLogger(logging.getLogger('game')),
            BaseLogger: BaseLogger(logging.getLogger())
        }
