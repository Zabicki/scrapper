import os
import logging

SCRAPPER_LOGS_BASE_DIR = os.environ.get("SCRAPPER_LOGS")

if not SCRAPPER_LOGS_BASE_DIR:
    raise EnvironmentError("SCRAPPER_LOGS environment variable is not set.")

LOG_FILE_PATH = os.path.join(SCRAPPER_LOGS_BASE_DIR, "scrapper.log")

log_directory = os.path.dirname(LOG_FILE_PATH)

try:
    os.makedirs(log_directory, exist_ok=True)
except OSError as e:
    logging.error(f"Error creating log directory {log_directory}: {e}")

try:
    with open(LOG_FILE_PATH, 'a') as f:
        pass
except IOError as e:
    logging.error(f"Error creating log file {LOG_FILE_PATH}: {e}")
