import warnings
import logging
from logging.handlers import RotatingFileHandler
from os import path, makedirs
from sys import stdout

SCRIPT_DIR = path.dirname(path.abspath(__file__))

LOG_LEVEL = logging.INFO
LOG_FILE = path.join(SCRIPT_DIR, "untappd_photos.log")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3

DISPLAY_DURATION = 10000  # in seconds
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
BACKGROUND_COLOR = (0, 0, 0)

AUTO_START_HOUR = 7  # 7 AM
AUTO_STOP_HOUR = 22  # 10 PM

MEDIA_DIR = path.join(SCRIPT_DIR, "media")
PHOTOS_DIR = path.join(MEDIA_DIR, "photos")

if not path.exists(MEDIA_DIR):
    makedirs(MEDIA_DIR)

warnings.filterwarnings("ignore", message="Your system is neon capable but pygame was not built with support for it.", category=RuntimeWarning)

logger = logging.getLogger("untappd_photos")
logger.setLevel(LOG_LEVEL)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(stream=stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.info("CONFIG LOADED")
