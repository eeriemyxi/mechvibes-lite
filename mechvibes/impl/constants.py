from __future__ import annotations
import os
import sys
from enum import Enum, auto
from pathlib import Path
import typing as t

import mergedeep  # type: ignore
import yaml

from mechvibes.impl.errors import EventNumberNotProvided


class AppConfig(t.TypedDict):
    core: AppConfigCore
    active_theme: AppConfigActiveTheme
    keys: dict[int, AppConfigKeyConfig]


class AppConfigCore(t.TypedDict):
    input_event_code: int


class AppConfigActiveTheme(t.TypedDict):
    id: str
    max_volume: int


class AppConfigKeyConfig(t.TypedDict):
    enabled: bool
    volume: int


class ThemeAudioMode(Enum):
    SINGLE = auto()
    MULTI = auto()


class Platform(Enum):
    DARWIN = auto()
    LINUX = auto()
    WIN32 = auto()


SCRIPT_DIRECTORY_PATH: Path = Path(os.path.dirname(os.path.realpath(__file__))).parents[
    1
]

if sys.platform == "darwin":
    PLATFORM = Platform.DARWIN
elif sys.platform == "linux":
    PLATFORM = Platform.LINUX
elif sys.platform == "win32":
    PLATFORM = Platform.WIN32

with open(SCRIPT_DIRECTORY_PATH / "configuration.yml") as config_buf:
    CONFIG: AppConfig = yaml.safe_load(config_buf)

MECHVIBES_CONFIG_OVERWRITES: AppConfig = yaml.safe_load(
    os.environ.get("MECHVIBES_CONFIG_OVERWRITES", "{}")
)
if MECHVIBES_CONFIG_OVERWRITES:
    mergedeep.merge(CONFIG, MECHVIBES_CONFIG_OVERWRITES)  # type: ignore

if PLATFORM == Platform.LINUX:
    try:
        INPUT_EVENT_CODE: int = CONFIG["core"]["input_event_code"]
        EVENT_PATH = Path("/dev/input")
    except IndexError:
        raise EventNumberNotProvided(
            "You must pass device event number of a keyboard "
            "in `configuration.yml`. Please follow the instructions in README.md "
            "given for Linux users."
        )

SUPPORTED_PLATFORMS: tuple[Platform] = (Platform.LINUX,)
SUPPORTED_AUDIO_FORMATS: tuple[str, ...] = (".wav", ".mp3", ".ogg", ".flac")

THEME_SETS_DIR_PATH: Path = SCRIPT_DIRECTORY_PATH / "themes"
CONFIG_FILE_NAME: str = "config.json"

ACTIVE_THEME_ID: str = CONFIG["active_theme"]["id"]
ACTIVE_THEME_MAX_VOLUME: int = CONFIG["active_theme"]["max_volume"]

KEY_AUDIO_SETTINGS: dict[int, AppConfigKeyConfig] = CONFIG["keys"]
