import logging
import os

LOG_FILE = os.environ.get("SCRAPPER_LOGS") + "/scrapper.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(name):
    return logging.getLogger(name)