from logging import Logger


class BaseLogger:

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    @property
    def logger(self):
        return self._logger
