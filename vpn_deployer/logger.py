import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "/var/log/vpn_deployer"
LOG_FILE = os.path.join(LOG_DIR, "vpn_deployer.log")

# Max size per log file: 5MB, keep 3 backups
MAX_LOG_SIZE = 5 * 1024 * 1024
BACKUP_COUNT = 3


def get_logger(name: str):
    """
    Returns a logger with the given name.
    Automatically sets up rotating file logs and console output.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')

        # Console log
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File log with rotation
        fh = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
