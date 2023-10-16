from __future__ import annotations

import json
import typing as t

import pyglet.media  # type: ignore

from mechvibes.impl import constants
from mechvibes.impl.struct.audio import DirectAudio, LocativeAudio

if t.TYPE_CHECKING:
    from pathlib import Path


class Config(t.TypedDict):
    key_define_type: str
    sound: str
    defines: dict[int, list[int] | str | None]


class ConfigParser:
    def __init__(self, base_path: Path, theme_dir_name: str, config_file_name: str):
        self.base_path = base_path
        self.theme_path = self.base_path / theme_dir_name
        self.config_path = self.theme_path / config_file_name

        self.config = self.parse_config(self.config_path)

    @property
    def audio_mode(self) -> constants.ThemeAudioMode | None:
        if self.config["key_define_type"] == "multi":
            return constants.ThemeAudioMode.MULTI
        elif self.config["key_define_type"] == "single":
            return constants.ThemeAudioMode.SINGLE

    @property
    def sfx_pack_path(self) -> None | Path:
        if self.audio_mode == constants.ThemeAudioMode.SINGLE:
            return self.theme_path / self.config["sound"]

    def parse_config(self, config_path: Path) -> Config:
        with open(str(config_path), "r") as buffer:
            return json.load(buffer)

    def iter_audio_indices(self):
        if self.audio_mode == constants.ThemeAudioMode.MULTI:
            for code, filename in self.config["defines"].items():
                if (
                    filename
                    and isinstance(filename, str)
                    and filename[filename.index(".") :]
                    in constants.SUPPORTED_AUDIO_FORMATS
                ):
                    audio_path = self.theme_path / filename
                    yield DirectAudio(
                        playable=pyglet.media.load(audio_path, streaming=False),  # type: ignore
                        path=audio_path,
                        scancode=int(code),
                    )
        elif self.audio_mode == constants.ThemeAudioMode.SINGLE:
            for code, timeline in self.config["defines"].items():
                if timeline and isinstance(timeline, list):
                    start, end = timeline[:2]
                    yield LocativeAudio(timeline=(start, end), scancode=int(code))
