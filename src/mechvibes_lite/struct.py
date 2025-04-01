import pathlib
from dataclasses import dataclass
from enum import Enum, auto

import kisesi

from mechvibes_lite import util

log = kisesi.get_logger(__name__)


class PlaybackType(Enum):
    SINGLE_FILE = auto()
    MULTI_FILE = auto()

    @classmethod
    def from_str(cls, type_s: str):
        if type_s == "single":
            return cls.SINGLE_FILE
        if type_s == "multi":
            return cls.MULTI_FILE
        raise ValueError

    @classmethod
    def from_config(cls, config: dict):
        return cls.from_str(config["key_define_type"])


@dataclass
class Configuration:
    theme_dir: pathlib.Path | str
    theme_folder_name: str
    wskey_host: str
    wskey_port: int

    event_path_base: pathlib.Path | str = pathlib.Path("/dev/input/")
    event_id: str = None

    def __post_init__(self):
        if isinstance(self.theme_dir, str):
            self.theme_dir = pathlib.Path(self.theme_dir).expanduser().resolve()
        if isinstance(self.event_path_base, str):
            self.event_path_base = (
                pathlib.Path(self.event_path_base).expanduser().resolve()
            )

        self.event_id = util.parse_event_id(self.event_id)

        self.event_path = (
            self.event_path_base / self.event_id if self.event_id else None
        )
        self.theme_path = self.theme_dir / self.theme_folder_name

        self.ensure_files_exist()

    def ensure_files_exist(self) -> None:
        if not self.theme_dir.exists():
            raise FileNotFoundError(
                f"theme_dir specified as '{self.theme_dir}' but it doesn't exist."
            )
        if not self.theme_path.exists():
            raise KeyError(
                f"theme_folder_name specified as '{self.theme_folder_name}', but '{self.theme_path}' doesn't exist"
            )

    @classmethod
    def from_config(cls, config: str):
        import configparser
        import sys

        confparser = configparser.ConfigParser()
        confparser.read_string(config)

        event_id = None
        if sys.platform == "linux":
            event_id = confparser.get("wskey", "event_id")

        return cls(
            confparser.get("theme", "theme_dir"),
            confparser.get("theme", "folder_name"),
            confparser.get("wskey", "host"),
            confparser.get("wskey", "port"),
            event_id=event_id,
        )


@dataclass
class Theme:
    name: str
    id: str
    includes_numpad: bool
    type: PlaybackType
    sound: pathlib.Path | None
    defines: dict[int, str | tuple[int, int]]
    base_path: pathlib.Path | None

    @staticmethod
    def _parse_defines(pl_type: PlaybackType, defines: dict, base_path: pathlib.Path):
        if pl_type is PlaybackType.SINGLE_FILE:
            return {int(code): tuple(stamp) for code, stamp in defines.items() if stamp}
        if pl_type is PlaybackType.MULTI_FILE:
            return {
                int(code): base_path / path for code, path in defines.items() if path
            }
        return None

    @classmethod
    def from_config(cls, config: dict | pathlib.Path, base_path: pathlib.Path | None):
        if isinstance(config, pathlib.Path):
            import json

            with open(config) as conf:
                config = json.load(conf)

        log.debug("Trying to construct Theme from: %s", config)
        pl_type = PlaybackType.from_config(config)
        defines = cls._parse_defines(pl_type, config["defines"], base_path)

        return cls(
            name=config["name"],
            id=config["id"],
            type=pl_type,
            includes_numpad=config["includes_numpad"],
            sound=(
                base_path / config["sound"]
                if pl_type is PlaybackType.SINGLE_FILE
                else None
            ),
            defines=defines,
            base_path=base_path,
        )
