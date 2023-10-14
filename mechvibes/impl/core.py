from functools import partial
from pathlib import Path
from threading import Thread

import pyglet.app

from mechvibes.impl import constants
from mechvibes.impl.audio_handler import AudioHandler
from mechvibes.impl.errors import ListenerNotFound
from mechvibes.impl.listeners import DarwinListener, LinuxListener, Win32Listener
from mechvibes.impl.parser import ConfigParser


class App:
    def __init__(self):
        self.event_code = constants.EVENT_CODE

    def instigate_listener(
        self, platform: constants.Platform, *, run_in_thread: bool = False
    ) -> bool:
        if not self.platform_is_supported(platform):
            raise NotImplementedError("Operating system unsupported.")

        parser = ConfigParser(
            constants.SCRIPT_DIRECTORY_PATH,
            constants.THEME_DIR_NAME,
            constants.CONFIG_FILE_NAME,
        )
        audio_handler = AudioHandler(parser)

        match platform:
            case constants.Platform.DARWIN:
                ...
            case constants.Platform.LINUX:
                listener = LinuxListener(
                    constants.EVENT_PATH, self.event_code, audio_handler
                )
                if run_in_thread:
                    listener_thread = Thread(target=listener.listen, daemon=True)
                    listener_thread.start()
                else:
                    listener.listen()
            case constants.Platform.WIN32:
                ...
            case _:
                raise ListenerNotFound("Unknown operating system.")

        return True

    def on_pyglet_event_loop_start(self, platform):
        Thread(
            target=self.instigate_listener,
            args=(platform,),
            kwargs=dict(run_in_thread=True),
            daemon=True,
        ).start()

    def run(self, platform: constants.Platform, *, event_code: None | int = None):
        if event_code:
            self.event_code = event_code

        event_loop = pyglet.app.EventLoop()
        event_loop.on_enter = partial(self.on_pyglet_event_loop_start, platform)
        event_loop.run(interval=None)

    def platform_is_supported(self, platform: constants.Platform) -> bool:
        if platform in constants.SUPPORTED_PLATFORMS:
            return True
        else:
            return False
