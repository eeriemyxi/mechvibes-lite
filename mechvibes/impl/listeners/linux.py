from __future__ import annotations

import logging
import typing as t

import evdev  # type: ignore

from mechvibes.impl import constants
from mechvibes.impl.abc.listener import AbstractListener
from mechvibes.impl.struct.audio import DirectAudio, LocativeAudio

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
                key: evdev.KeyEvent = evdev.categorize(event)  # type: ignore

                if key.keystate == evdev.KeyEvent.key_down:
                    try:
                        struct = self.audio_handler.addressed_audio_indices[
                            key.scancode  # type: ignore
                        ]
                        if (
                            self.audio_handler.parser.audio_mode
                            == constants.ThemeAudioMode.SINGLE
                        ):
                            if (
                                isinstance(struct, LocativeAudio)
                                and self.audio_handler.sfx_pack_source
                            ):
                                self.audio_handler.play(
                                    self.audio_handler.sfx_pack_source,
                                    timeline=struct.timeline,
                                    run_in_thread=False,
                                )
                        elif (
                            self.audio_handler.parser.audio_mode
                            == constants.ThemeAudioMode.MULTI
                        ) and isinstance(struct, DirectAudio):
                            self.audio_handler.play(
                                struct.playable, run_in_thread=False
                            )
                    except KeyError:
                        logger.critical(
                            "Audio unknown for key scancode %s.",
                            key.scancode,  # type: ignore
                        )
