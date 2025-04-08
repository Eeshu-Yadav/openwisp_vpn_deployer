import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

LOG_DIR = os.getenv("LOG_DIR", "./logs")

os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name):
    """
    Returns a configured logger for the given module or component name.
    
    - Logs are written to a file in the LOG_DIR directory.
    - Log rotation is set up to rotate once the log file reaches 5MB,
      with up to 5 backup files.
    - Also outputs logs to console during development.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    log_file = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

if __name__ == "__main__":
    test_logger = get_logger("test_logger")
    test_logger.debug("This is a DEBUG message")
    test_logger.info("This is an INFO message")
    test_logger.warning("This is a WARNING message")
    test_logger.error("This is an ERROR message")
    test_logger.critical("This is a CRITICAL message")
