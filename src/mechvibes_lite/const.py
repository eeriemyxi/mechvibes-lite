import configparser
import logging
import pathlib
import sys

from mechvibes_lite import util

log = logging.getLogger(__name__)

APP_NAME = "mechvibes-lite"

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

if sys.platform == "linux":
    EVENT_PATH_BASE = pathlib.Path("/dev/input/")
    EVENT_ID = util.parse_event_id(CONFIG.get("general", "event_id"))
    EVENT_PATH = EVENT_PATH_BASE / EVENT_ID

WSKEY_HOST = CONFIG.get("wskey", "host")
WSKEY_PORT = CONFIG.get("wskey", "port")

THEME_DIR = pathlib.Path(CONFIG.get("general", "theme_dir")).expanduser().resolve()
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
