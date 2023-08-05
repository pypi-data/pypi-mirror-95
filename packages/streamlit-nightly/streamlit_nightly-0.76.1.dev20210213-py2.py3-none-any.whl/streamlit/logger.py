# Copyright 2018-2021 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logging module."""

import inspect
import logging
import sys
import time
from typing import Dict

from streamlit import development
from streamlit import config

# Loggers for each name are saved here.
LOGGERS = {}  # type: Dict[str, logging.Logger]

# The global log level is set here across all names.
LOG_LEVEL = logging.INFO

DEFAULT_LOG_MESSAGE = "%(asctime)s %(levelname) -7s " "%(name)s: %(message)s"


def set_log_level(level):
    """Set log level."""
    logger = get_logger(__name__)

    if isinstance(level, str):
        level = level.upper()
    if level == "CRITICAL" or level == logging.CRITICAL:
        log_level = logging.CRITICAL
    elif level == "ERROR" or level == logging.ERROR:
        log_level = logging.ERROR
    elif level == "WARNING" or level == logging.WARNING:
        log_level = logging.WARNING
    elif level == "INFO" or level == logging.INFO:
        log_level = logging.INFO
    elif level == "DEBUG" or level == logging.DEBUG:
        log_level = logging.DEBUG
    else:
        msg = 'undefined log level "%s"' % level
        logger.critical(msg)
        sys.exit(1)

    for log in LOGGERS.values():
        log.setLevel(log_level)

    global LOG_LEVEL
    LOG_LEVEL = log_level


def setup_formatter(logger):
    """Set up the console formatter for a given logger."""

    # Deregister any previous console loggers.
    if hasattr(logger, "streamlit_console_handler"):
        logger.removeHandler(logger.streamlit_console_handler)

    logger.streamlit_console_handler = logging.StreamHandler()

    if config._config_file_has_been_parsed:
        # logger is required in ConfigOption.set_value
        # Getting the config option before the config file has been parsed
        # can create an infinite loop
        message_format = config.get_option("logger.messageFormat")
    else:
        message_format = DEFAULT_LOG_MESSAGE
    formatter = logging.Formatter(fmt=message_format)
    formatter.default_msec_format = "%s.%03d"
    logger.streamlit_console_handler.setFormatter(formatter)

    # Register the new console logger.
    logger.addHandler(logger.streamlit_console_handler)


def update_formatter():
    for log in LOGGERS.values():
        setup_formatter(log)


def init_tornado_logs():
    """Initialize tornado logs."""
    global LOGGER

    # http://www.tornadoweb.org/en/stable/log.html
    logs = ["access", "application", "general"]
    for log in logs:
        name = "tornado.%s" % log
        get_logger(name)

    logger = get_logger(__name__)
    logger.debug("Initialized tornado logs")


def get_logger(name):
    """Return a logger.

    Parameters
    ----------
    name : str
        The name of the logger to use. You should just pass in __name__.

    Returns
    -------
    Logger

    """
    if name in LOGGERS.keys():
        return LOGGERS[name]

    if name == "root":
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(name)

    logger.setLevel(LOG_LEVEL)
    logger.propagate = False
    setup_formatter(logger)

    LOGGERS[name] = logger

    return logger
