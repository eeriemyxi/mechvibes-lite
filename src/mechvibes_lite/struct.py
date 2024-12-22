import logging
import pathlib
from dataclasses import dataclass
from enum import Enum, auto

log = logging.getLogger(__name__)


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
            sound=base_path / config["sound"]
            if pl_type is PlaybackType.SINGLE_FILE
            else None,
            defines=defines,
            base_path=base_path,
        )
