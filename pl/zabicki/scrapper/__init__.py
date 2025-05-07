import os

SCRAPPER_LOGS_BASE_DIR = os.environ.get("SCRAPPER_LOGS")

if not SCRAPPER_LOGS_BASE_DIR:
    raise EnvironmentError("SCRAPPER_LOGS environment variable is not set.")

LOG_FILE_PATH = os.path.join(SCRAPPER_LOGS_BASE_DIR, "scrapper.log")

log_directory = os.path.dirname(LOG_FILE_PATH)

os.makedirs(log_directory, exist_ok=True)
with open(LOG_FILE_PATH, 'a') as f:
    pass
