from pathlib import Path

import evdev

from impl import constants
from impl.abc.listener import AbstractListener


class LinuxListener(AbstractListener):
    def __init__(self, event_path, event_code, audio_handler):
        self.event_path = event_path
        self.event_code = event_code
        self.audio_handler = audio_handler
        self.device_path = str(event_path / f"event{event_code}")
        self.device = evdev.InputDevice(self.device_path)

    def listen(self):
        for event in self.device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key = evdev.categorize(event)

                if key.keystate == evdev.KeyEvent.key_down:
                    if (
                        self.audio_handler.parser.audio_mode
                        == constants.ThemeAudioMode.SINGLE
                    ):
                        struct = self.audio_handler.addressed_audio_indices[
                            key.scancode
                        ]
                        self.audio_handler.play(
                            self.audio_handler.sfx_pack_source,
                            timeline=struct.timeline,
                            run_in_thread=True,
                        )
                    elif (
                        self.audio_handler.parser.audio_mode
                        == constants.ThemeAudioMode.MULTI
                    ):
                        struct = self.audio_handler.addressed_audio_indices[
                            key.scancode
                        ]
                        self.audio_handler.play(struct.playable)
