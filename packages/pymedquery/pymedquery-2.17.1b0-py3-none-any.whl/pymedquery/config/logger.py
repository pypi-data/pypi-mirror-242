"""
This is a customized logger for the database project.
"""
import logging
from colorlog import ColoredFormatter
import os
from pathlib import Path

from typing import Any

# TODO: inlcude comments

# Setting color logs
SUCCESS: int = 21
FAIL: int = 22
PIPE: int = 55
LOG_LEVEL = logging.INFO
LOG_LEVEL_E = logging.WARNING
#  LOGFORMAT = '%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s'
LOGFORMAT: str = "%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
LOGFORMAT_ERROR: str = "%(log_color)s%(asctime)-8s%(reset)s | %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

ROOT: str = os.getcwd()  # os.environ['PYTHONPATH']

# Adding file path for error logs and levels above
FILE_PATH: str = os.path.join(ROOT, "docs/logs/level_errors_logs.log")
Path(FILE_PATH).parent.mkdir(
    exist_ok=True, parents=True
)  # It is sad with non existent parents

logging.addLevelName(SUCCESS, "SUCCESS")
logging.addLevelName(FAIL, "FAIL")
logging.addLevelName(PIPE, "PIPE")


def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kws)


def fail(self, message, *args, **kws):
    if self.isEnabledFor(FAIL):
        self._log(FAIL, message, args, **kws)


def pipe(self, message, *args, **kws):
    if self.isEnabledFor(PIPE):
        self._log(PIPE, message, args, **kws)


logging.Logger.success = success
logging.Logger.fail = fail
logging.Logger.pipe = pipe
logging.root.setLevel(LOG_LEVEL)

formatter = ColoredFormatter(
    LOGFORMAT,
    log_colors={
        "DEBUG": "white,bg_black",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_black",
        "SUCCESS": "bold_green",
        "FAIL": "white,bg_black",
        "PIPE": "green",
    },
)

e_formatter = ColoredFormatter(
    LOGFORMAT_ERROR,
    log_colors={
        "DEBUG": "white,bg_black",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red,bg_black",
        "SUCCESs": "bold_green",
        "FAIL": "white, bg_black",
        "PIPE": "green",
    },
)

stream = logging.StreamHandler()
file_handler = logging.FileHandler(FILE_PATH)

stream.setLevel(LOG_LEVEL)
# TODO: Only save loglevel error to file
file_handler.setLevel(LOG_LEVEL_E)

stream.setFormatter(formatter)
file_handler.setFormatter(e_formatter)


def get_logger(name) -> Any:
    log = logging.getLogger(name)
    log.setLevel(LOG_LEVEL)
    if log.hasHandlers():
        log.handlers.clear()
    log.addHandler(stream)
    log.addHandler(file_handler)
    return log
