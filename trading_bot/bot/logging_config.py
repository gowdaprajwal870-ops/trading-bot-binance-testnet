"""
logging_config.py
Sets up logging so all API requests, responses, and errors
are written to a log file (bot.log) as well as printed to console.
"""

import logging
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", "bot.log")


def setup_logger():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if setup_logger() is called more than once
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def log_and_print(message, level="info"):
    """Prints to console AND writes to the log file."""
    print(message)
    if level == "error":
        logger.error(message)
    else:
        logger.info(message)
