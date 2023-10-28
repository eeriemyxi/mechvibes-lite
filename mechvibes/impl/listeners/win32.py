import logging

from mechvibes.impl import constants
from mechvibes.impl.audio_handler import AudioHandler

if constants.PLATFORM == constants.Platform.WIN32:  # type: ignore
    import keyboard  # type: ignore

from mechvibes.impl.abc.listener import AbstractListener

logger = logging.getLogger(__name__)


class Win32Listener(AbstractListener):
    def __init__(self, audio_handler: AudioHandler):
        self.audio_handler = audio_handler

    def listen(self) -> None:
        logger.info("Listening for input events started.")
        while True:
            event = keyboard.read_event()
            if (
                event.event_type == keyboard.KEY_UP
                and self.audio_handler.parser.audio_mode
            ):
                try:
                    self.play_key_for(
                        scancode=event.scan_code,
                        audio_mode=self.audio_handler.parser.audio_mode,
                        run_in_thread=False,
                    )
                except KeyError:
                    logger.critical(
                        "Audio unknown for key scancode %s.",
                        event.scan_code,  # type: ignore
                    )
