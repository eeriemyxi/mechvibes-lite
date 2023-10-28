from abc import ABC, abstractmethod

from mechvibes.impl.struct.audio import DirectAudio, LocativeAudio


class AbstractListener(ABC):
    @abstractmethod
    def __init__(self, audio_handler):
        self.audio_handler

    @abstractmethod
    def listen(self) -> None:
        pass

    def play_key_for(self, *, platform, scancode, audio_mode):
        struct = self.audio_handler.addressed_audio_indices[scancode]

        if (
            self.audio_handler.parser.audio_mode == audio_mode
            and isinstance(struct, LocativeAudio)
            and self.audio_handler.sfx_pack_source
        ):
            self.audio_handler.play(
                self.audio_handler.sfx_pack_source,
                timeline=struct.timeline,
                run_in_thread=False,
            )
        elif (self.audio_handler.parser.audio_mode == audio_mode) and isinstance(
            struct, DirectAudio
        ):
            self.audio_handler.play(struct.playable, run_in_thread=False)
