from __future__ import annotations

import logging
import os
import sys
import typing as t
from enum import Enum, auto
from pathlib import Path

import mergedeep  # type: ignore
import yaml
from rich.logging import RichHandler

from mechvibes.impl.errors import EventNumberNotProvidedError

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


class AppConfigCore(t.TypedDict):
    input_event_code: int


class AppConfigActiveTheme(t.TypedDict):
    id: str
    max_volume: int


class AppConfigKeyConfig(t.TypedDict):
    enabled: bool
    volume: int


class AppConfig(t.TypedDict):
    core: AppConfigCore
    active_theme: AppConfigActiveTheme
    keys: dict[int, AppConfigKeyConfig]


class ThemeAudioMode(Enum):
    SINGLE = auto()
    MULTI = auto()


class Platform(Enum):
    DARWIN = auto()
    LINUX = auto()
    WIN32 = auto()


SCRIPT_DIRECTORY_PATH: Path = Path(__file__).parents[1]

CONFIG_DIRECTORY_NAME = "mechvibes-lite"
CONFIG_FILE_NAME = "configuration.yml"


def find_app_config_path_from(paths: tuple[Path, ...]) -> Path:
    for path in paths:
        if path.exists():
            logger.info("Using path `%s` for configuration lookup.", path)
            return path
        logger.info("Cannot find configuration file in `%s`. Trying next path...", path)

    error = FileNotFoundError(
        "No possible paths to configuration file found. "
        "Please create a configuration file."
    )
    error.add_note("You can create a configuration file in the following paths:")
    for path in paths:
        error.add_note(f"\t{path / CONFIG_FILE_NAME}")
    error.add_note(
        "Also note that you can generate the content for a default "
        "configuration file with `mvibes --generate-config` command."
    )
    raise error from None


if sys.platform == "darwin":
    PLATFORM = Platform.DARWIN
elif sys.platform == "linux":
    PLATFORM = Platform.LINUX
    APP_CONFIGURATION_PATHS = (
        Path("/etc") / CONFIG_DIRECTORY_NAME,
        Path(os.environ.get("XDG_CONFIG_HOME", Path(os.environ["HOME"]) / ".config"))
        / CONFIG_DIRECTORY_NAME,
        SCRIPT_DIRECTORY_PATH,
    )
    APP_CONFIG_PATH = find_app_config_path_from(APP_CONFIGURATION_PATHS)
elif sys.platform == "win32":
    PLATFORM = Platform.WIN32
    APP_CONFIGURATION_PATHS = (
        Path(os.environ["APPDATA"]) / CONFIG_DIRECTORY_NAME,
        SCRIPT_DIRECTORY_PATH,
    )
    APP_CONFIG_PATH = find_app_config_path_from(APP_CONFIGURATION_PATHS)

with open(APP_CONFIG_PATH / CONFIG_FILE_NAME) as config_buf:
    CONFIG: AppConfig = yaml.safe_load(config_buf)

MECHVIBES_CONFIG_OVERWRITES: AppConfig = yaml.safe_load(
    os.environ.get("MECHVIBES_CONFIG_OVERWRITES", "{}")
)
if MECHVIBES_CONFIG_OVERWRITES:
    logger.info("Merging configuration overwrites...")
    mergedeep.merge(CONFIG, MECHVIBES_CONFIG_OVERWRITES)  # type: ignore

if PLATFORM == Platform.LINUX:
    try:
        INPUT_EVENT_CODE: int = CONFIG["core"]["input_event_code"]
        logger.debug("Input event ID has been set to: %s", INPUT_EVENT_CODE)
        EVENT_PATH = Path("/dev/input")
    except IndexError:
        raise EventNumberNotProvidedError(
            "You must pass device event number of a keyboard "
            f"in `{CONFIG_FILE_NAME}`. Please follow the instructions in `README.md` "
            "given for Linux users."
        ) from None

SUPPORTED_PLATFORMS: tuple[Platform, ...] = (Platform.LINUX, Platform.WIN32)
SUPPORTED_AUDIO_FORMATS: tuple[str, ...] = (".wav", ".mp3", ".ogg", ".flac")

THEME_CONFIG_FILE_NAME = "config.json"
THEME_SETS_DIR_PATH: Path = APP_CONFIG_PATH / "themes"
if not THEME_SETS_DIR_PATH.exists():
    THEME_SETS_DIR_PATH.mkdir()

ACTIVE_THEME_ID: str = CONFIG["active_theme"]["id"]
ACTIVE_THEME_MAX_VOLUME: int = CONFIG["active_theme"]["max_volume"]

KEY_AUDIO_SETTINGS: dict[int, AppConfigKeyConfig] = CONFIG["keys"]
