"""Colorful and Simple Logger: cologs"""

__version__ = "0.3"

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

COLOGS_FOLDER = "logs"
COLOGS_FILE = "cologs.log"


class CustomFormatter(logging.Formatter):
    """Custom Formatter that adds Colored outputs for STDOUT and an informative format string to standard Python logger"""
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_string = "[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_string + reset,
        logging.INFO: green + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
        logging.CRITICAL: bold_red + format_string + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%a, %d %b %Y %H:%M:%S")
        return formatter.format(record)


def get_cologs(logger_name="", default_level=logging.DEBUG):
    """
    Create a logger that sends its output to STDOUT and
    `cologs.COLOGS_FOLDER/cologs.COLOGS_FILE`. You can change the constants if you'd like.
    The `cologs.COLOGS_FILE` file is rotated when it gets large enough.

    Args:
        `logger_name`: name of logger. multiple calls to this function with same `logger_name`
            returns the same cologs logger. by default `""`
        `default_level`: default level for logging, by default `logging.DEBUG`

    Returns:
        cologs logger

    ```py
    from cologs import get_cologs

    cologs = get_cologs()
    cologs.debug("Debug message")
    cologs.info("Info message")
    cologs.warning("Warning message")
    cologs.error("Error message")
    cologs.critical("Critical message")
    ```
    """
    folder_path = COLOGS_FOLDER
    log_file_name = COLOGS_FILE
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    log_file_path = os.path.join(folder_path, log_file_name)
    cologs = logging.getLogger(logger_name)
    cologs.setLevel(default_level)
    fh = RotatingFileHandler(log_file_path, maxBytes=2000000, backupCount=10)
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(CustomFormatter.format_string, datefmt="%a, %d %b %Y %H:%M:%S")
    fh.setFormatter(formatter)
    sh.setFormatter(CustomFormatter())
    cologs.addHandler(fh)
    cologs.addHandler(sh)

    return cologs
