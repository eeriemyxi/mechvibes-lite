import sys
from pathlib import Path
from threading import Thread

import pyglet.app

from impl import constants
from impl.audio_handler import AudioHandler
from impl.errors import ListenerNotFound
from impl.listeners import DarwinListener, LinuxListener, Win32Listener
from impl.parser import ConfigParser


class App:
    def __init__(self):
        ...

    def instigate_listener(
        self, platform: constants.Platform, *, run_in_thread: bool = False
    ) -> bool:
        if not self.platform_is_supported(platform):
            raise NotImplementedError("Operating system unsupported.")

        parser = ConfigParser(
            Path(constants.SCRIPT_DIRECTORY),
            constants.THEME_DIR_NAME,
            constants.CONFIG_FILE_NAME,
        )
        audio_handler = AudioHandler(parser)

        match platform:
            case constants.Platform.DARWIN:
                ...
            case constants.Platform.LINUX:
                listener = LinuxListener(
                    constants.EVENT_PATH, constants.EVENT_CODE, audio_handler
                )
                listener.listen()
            case constants.Platform.WIN32:
                ...
            case _:
                raise ListenerNotFound("Unknown operating system.")

        return True

    def run_pyglet_event_loop(self):
        pyglet.app.run()

    def platform_is_supported(self, platform: constants.Platform) -> bool:
        if platform in constants.SUPPORTED_PLATFORMS:
            return True
        else:
            return False
