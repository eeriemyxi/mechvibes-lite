import json
from pathlib import Path

import pyglet.media

from impl import constants
from impl.struct.audio import DirectAudio, LocativeAudio


class ConfigParser:
    def __init__(
        self, base_path: Path, theme_path: Path, config_path: Path, audio_handler
    ):
        self.base_path = base_path
        self.theme_path = theme_path
        self.config_path = config_path
        self.audio_handler = audio_handler

        self.config = self.parse_config(self.config_path)

    @property
    def audio_mode(self) -> constants.ThemeAudioMode:
        if self.config["key_define_type"] == "multi":
            return constants.ThemeAudioMode.MULTI
        else:
            return constants.ThemeAudioMode.SINGLE

    @property
    def sfx_pack_path(self) -> None | Path:
        if self.audio_mode == constants.ThemeAudioMode.SINGLE:
            return self.theme_path / self.config["sound"]

    def parse_config(self, config_path) -> dict:
        with open(str(config_path), "r") as buffer:
            return json.load(buffer)

    def iter_audio_indices(self):
        if self.audio_mode == constants.ThemeAudioMode.MULTI:
            for code, filename in self.config["defines"].items():
                if filename[filename.index(".") :] in constants.SUPPORTED_AUDIO_FORMATS:
                    audio_path = self.theme_path / filename
                    yield DirectAudio(
                        playable=pyglet.media.Source(audio_path, streaming=False),
                        path=audio_path,
                        keycode=code,
                    )
        elif self.audio_mode == constants.ThemeAudioMode.SINGLE:
            for code, timeline in self.config["defines"].items():
                yield LocativeAudio(
                    self.audio_handler.sfx_pack_source, timeline=timeline, keycode=code
                )
