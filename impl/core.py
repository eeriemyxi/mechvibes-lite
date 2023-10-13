from functools import partial
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
        print(type(audio_handler.sfx_pack_source))

        match platform:
            case constants.Platform.DARWIN:
                ...
            case constants.Platform.LINUX:
                listener = LinuxListener(
                    constants.EVENT_PATH, constants.EVENT_CODE, audio_handler
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

    def on_event_loop_start(self, platform):
        print(platform)
        Thread(
            target=self.instigate_listener,
            args=platform,
            kwargs=dict(run_in_thread=True),
            daemon=True,
        ).start()

    def run_pyglet_event_loop(self, platform: constants.Platform):
        event_loop = pyglet.app.EventLoop()
        event_loop.on_enter = partial(self.on_event_loop_start, (platform,))
        event_loop.run()

    def platform_is_supported(self, platform: constants.Platform) -> bool:
        if platform in constants.SUPPORTED_PLATFORMS:
            return True
        else:
            return False
