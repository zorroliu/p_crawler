# -*- coding: utf-8 -*-

import os
import sys
from enum import Enum
from loguru import logger
from base.config import default_config


class LogLevel(Enum):
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


class CustLogger:
    def __init__(self, name, log_path: str = None):
        self._bind_name = name
        self._logger = logger.bind(name=name)
        self._p_log_path(log_path)

        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{" \
                     "name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

        self._logger.remove()
        self._logger.add(self._log_path, rotation="00:00", format=log_format, encoding="utf-8")
        self._logger.add(sys.stdout, format=log_format)

    def _p_log_path(self, log_path):
        if log_path:
            self._log_path = log_path
        else:
            base_logs_path = default_config.get_val('base_logs_path')
            self._log_path = os.path.join(base_logs_path, self._bind_name, 'server.log')

    def log(self, message, level: LogLevel = LogLevel.INFO):
        getattr(self._logger, level.value)(message)


main_log: CustLogger = CustLogger('main')
http_log: CustLogger = CustLogger('http')
