import sys
from enum import Enum, auto
from pathlib import Path

from impl.errors import EventNumberNotProvided


class ThemeAudioMode(Enum):
    SINGLE = auto()
    MULTI = auto()


class Platform(Enum):
    DARWIN = auto()
    LINUX = auto()
    WIN32 = auto()


if sys.platform == "darwin":
    PLATFORM = Platform.DARWIN
elif sys.platform == "linux":
    try:
        EVENT_CODE = int(sys.argv[1])
        EVENT_PATH = Path("/dev/input")
    except IndexError:
        raise EventNumberNotProvided(
            "(Linux) You must pass device event number of a keyboard "
            "as a command line argument. Please follow the instructions in README.md "
            "given for Linux users."
        )
    PLATFORM = Platform.LINUX
elif sys.platform == "win32":
    PLATFORM = Platform.WIN32

SUPPORTED_PLATFORMS: tuple[Platform] = (Platform.LINUX,)
SUPPORTED_AUDIO_FORMATS: tuple[str] = (".wav", ".mp3", ".ogg", ".flac")

SCRIPT_DIRECTORY_PATH: str = sys.path[0]
THEME_DIR_NAME: str = "active_config"
CONFIG_FILE_NAME: str = "config.json"
