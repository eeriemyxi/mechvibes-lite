import sys
from enum import Enum
from pathlib import Path

from impl.errors import EventNumberNotProvided


class ThemeAudioMode(Enum):
    SINGLE = 1
    MULTI = 2


class Platform(Enum):
    DARWIN = 1
    LINUX = 2
    WIN32 = 3


if sys.platform == "darwin":
    PLATFORM = Platform.DARWIN
elif sys.platform == "linux":
    try:
        EVENT_CODE = int(sys.argv[1])
        EVENT_PATH = Path("/dev/input")
    except IndexError:
        raise EventNumberNotProvided(
            "(Linux) You must pass device event number of a keyboard as a command line argument"
        )
    PLATFORM = Platform.LINUX
elif sys.platform == "win32":
    PLATFORM = Platform.WIN32

SUPPORTED_PLATFORMS: tuple[Platform] = (Platform.LINUX, Platform.WIN32)
SUPPORTED_AUDIO_FORMATS = (".wav", ".mp3", ".ogg", ".flac")

SCRIPT_DIRECTORY = sys.path[0]
THEME_DIR_NAME = "active_config"
CONFIG_FILE_NAME = "config.json"
