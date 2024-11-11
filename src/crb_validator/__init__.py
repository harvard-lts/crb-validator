import logging
from logging.handlers import TimedRotatingFileHandler
import os
import socket
from datetime import datetime

LOG_FILE_BACKUP_COUNT = int(os.getenv('LOG_FILE_BACKUP_COUNT', '30'))
LOG_ROTATION = "midnight"

container_id = socket.gethostname()
timestamp = datetime.today().strftime('%Y-%m-%d')


def configure_logger(name):
    log_level = os.getenv("APP_LOG_LEVEL", "INFO")
    log_dir = os.getenv("LOG_DIR", "logs/")
    # create log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, "crb-app.log")
    formatter = logging.Formatter(
        '%(levelname)s - %(asctime)s - %(name)s - %(message)s')

    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        file_handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when=LOG_ROTATION,
            backupCount=LOG_FILE_BACKUP_COUNT
        )
        logger.addHandler(file_handler)
        file_handler.setFormatter(formatter)

    logger.setLevel(log_level)
    return logger
