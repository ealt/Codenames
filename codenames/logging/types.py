from pathlib import Path
from typing import TypeVar

from codenames.logging.base_logger import BaseLogger

ConfigMod = dict[str, str]
ConfigMods = dict[str, ConfigMod]
LoggingData = dict[str, Path | ConfigMods]
Logger = TypeVar('Logger', bound='BaseLogger')
