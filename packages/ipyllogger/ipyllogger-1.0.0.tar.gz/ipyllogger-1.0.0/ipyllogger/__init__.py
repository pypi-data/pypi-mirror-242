from typing import Literal

from ipyllogger.level import *
from ipyllogger.logger import AbstractLogger

from datetime import datetime


class Logger(AbstractLogger):

    def log(self, message: str, level: Literal['WARNING', 'ERROR'], reset=False) -> str:
        if not isinstance(message, str):
            raise ValueError("Log message must be a string")

        if level not in LEVELS:
            raise ValueError(
                "Invalid log level, must be one of: %s" % ", ".join(LEVELS))

        current_datetime = datetime.now()
        log = "%s: [%s] %s\n" % (
            level, current_datetime, message.strip()[:100])

        if level == ERROR:
            self._write_log(ERROR_LEVEL_FILE, log, reset)
        elif level == WARNING:
            self._write_log(WARNING_LEVEL_FILE, log, reset)

        return log.strip()

    def get_logs(self, level: Literal['WARNING', 'ERROR']) -> list[str]:
        filename = ERROR_LEVEL_FILE if level == ERROR else WARNING_LEVEL_FILE
        logs = self._read_logs(filename)

        def filter_logs(log: str):
            table_data = log.split(":")
            if table_data[0] == level:
                return log.replace('\n', '')

        current_level_logs = map(filter_logs, logs)

        return list(current_level_logs)
