import configparser
import logging
import pathlib

from mechvibes_lite import util

log = logging.getLogger(__name__)

APP_NAME = "mechvibes-lite"
SUPPORTED_AUDIO_FORMATS = (".ogg", ".wav")

CONFIG_HOME = util.get_config_path(APP_NAME)

if not CONFIG_HOME.exists():
    log.error("Configuration directory not found at '%s'", CONFIG_HOME)
    exit(1)

CONFIG_PATH = CONFIG_HOME / "config.ini"

if not CONFIG_PATH.exists():
    log.error("'config.ini' not found at '%s'", CONFIG_PATH)
    exit(1)

CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)

EVENT_PATH_BASE = pathlib.Path("/dev/input/")
EVENT_ID = CONFIG.get("general", "event_id")
if EVENT_ID.isdigit():
    EVENT_ID = f"event{EVENT_ID}"
EVENT_PATH = EVENT_PATH_BASE / EVENT_ID

WSKEY_PORT = CONFIG.get("wskey", "port")
WSKEY_HOST = CONFIG.get("wskey", "host")

THEME_DIR = pathlib.Path(CONFIG.get("general", "theme_dir")).resolve()
if not THEME_DIR.exists():
    log.error("theme_dir specified as '%s' but it doesn't exist.", THEME_DIR)
    exit(1)

THEME_FOLDER_NAME = CONFIG.get("theme", "folder_name")
THEME_PATH = THEME_DIR / THEME_FOLDER_NAME

if not THEME_PATH.exists():
    log.error(
        "theme_name specified as '%s', but '%s' doesn't exist",
        THEME_FOLDER_NAME,
        THEME_PATH,
    )
    exit(1)
