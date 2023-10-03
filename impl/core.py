import sys
from impl import constants
from impl.listeners import DarwinListener, LinuxListener, Win32Listener
from impl.errors import ListenerNotFound
import pyglet.app


class App:
    def __init__(self):
        ...

    def instigate_listener(self, platform: constants.Platform, *, run_in_thread: bool = False) -> bool:
        if not self.platform_is_supported(platform):
            raise NotImplementedError("Operating system unsupported.")

        match platform:
            case constants.Platform.DARWIN:
                ...
            case constants.Platform.LINUX:
                ...
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
