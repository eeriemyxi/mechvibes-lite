from __future__ import annotations

import logging
import typing as t

from mechvibes.impl import constants

if constants.PLATFORM == constants.Platform.LINUX:
    import evdev  # type: ignore


from mechvibes.impl.abc.listener import AbstractListener

logger = logging.getLogger(__name__)

if t.TYPE_CHECKING:
    from pathlib import Path

    from mechvibes.impl.audio_handler import AudioHandler


class LinuxListener(AbstractListener):
    def __init__(self, event_path: Path, event_code: int, audio_handler: AudioHandler):
        self.event_path = event_path
        self.event_code = event_code
        self.audio_handler = audio_handler
        self.device_path = str(event_path / f"event{event_code}")
        self.device = evdev.InputDevice(self.device_path)

        logger.info("Loaded Linux input event listener.")

    def listen(self) -> None:
        logger.info("Listening for input events started.")

        for event in self.device.read_loop():  # type: ignore
            if event.type == evdev.ecodes.EV_KEY:  # type: ignore
                key = t.cast(evdev.KeyEvent, evdev.categorize(event))  # type: ignore
                scancode = t.cast(int, key.scancode)  # type: ignore

                if (
                    key.keystate == evdev.KeyEvent.key_down
                    and self.audio_handler.parser.audio_mode
                ):
                    try:
                        self.play_key_for(
                            scancode=scancode,
                            audio_mode=self.audio_handler.parser.audio_mode,
                            run_in_thread=False,
                        )
                    except KeyError:
                        logger.critical(
                            "Audio unknown for key scancode %s.",
                            key.scancode,  # type: ignore
                        )
