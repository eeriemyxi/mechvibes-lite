import json
from impl import constants
import pathlib


class ConfigParser:
    def __init__(self):
        self.base_path = pathlib.Path(constants.SCRIPT_DIRECTORY)
        self.theme_path = self.base_path / constants.THEME_DIR_NAME
        self.config_path = self.theme_path / constants.CONFIG_FILE_NAME
       
        self.config = self.parse_config(self.config_path)

        self.audio_files = self.theme_path.glob("*.*!*.json")

    @property
    def audio_mode(self) -> constants.ThemeAudioMode:
        if self.config["key_define_type"] == "multi":
            return constants.ThemeAudioMode.MULTI
        else:
            return constants.ThemeAudioMode.SINGLE

    @property
    def sound_file(self) -> None | Path:
        if mode == constants.ThemeAudioMode.SINGLE:
            return self.theme_path / self.config["sound"]

    def parse_config(self, config_path) -> dict:
        with open(str(config_path), "r") as buffer:
            return json.load(buffer)