import logging

import keyboard

from mechvibes.impl import constants
from mechvibes.impl.abc.listener import AbstractListener

logger = logging.getLogger(__name__)


class Win32Listener(AbstractListener):
    def __init__(self, audio_handler):
        self.audio_handler = audio_handler

    def listen(self):
        logger.info("Listening for input events started.")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_UP:
                try:
                    self.play_key_for(
                        platform=constants.Platform.LINUX,
                        scancode=event.scan_code,
                        audio_mode=self.audio_handler.parser.audio_mode,
                    )
                except KeyError:
                    logger.critical(
                        "Audio unknown for key scancode %s.",
                        event.scan_code,  # type: ignore
                    )
