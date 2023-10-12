from impl import constants
import pyglet.media


class AudioHandler:
    def __init__(self):
        self.addressed_audio_indices = {
            item.keycode: item for item in self.parser.iter_audio_indices()
        }

    @property
    def sfx_pack_source(self):
        if constants.ThemeAudioMode.SINGLE:
            return pyglet.media.load(self.parser.sfx_pack_path, streaming=False)

    def play(
        self,
        playable,
        *,
        timeline: tuple[int, int] | None = None,
        run_in_thread: bool = False
    ):
        ...

    def _play_and_seek(self):
        ...
