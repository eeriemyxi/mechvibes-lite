from pathlib import Path

import evdev

from impl import constants


class LinuxListener:

    def __init__(self, event_path, event_code, audio_handler):
        self.event_path = event_path
        self.event_code = event_code
        self.audio_handler = audio_handler
        self.device_path = str(event_path / f'event{event_code}')
        self.device = evdev.InputDevice(self.device_path)

    def listen():
        for event in self.device.read_loop():
            if event.type == evdev.ecodes.