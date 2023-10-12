from impl import constants
import pyglet.media
import time
from threading import Thread


class AudioHandler:
    def __init__(self, parser):
        self.parser = parser
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
        if self.parser.audio_mode == constants.ThemeAudioMode.SINGLE:
            if run_in_thread:
                thread = Thread(target=self._play_and_seek, args=(playable, *self.timeline), daemon=True)
                thread.start()
            else:
                self._play_and_seek(playable, *self.timeline)
        elif self.parser.audio_mode == constants.ThemeAudioMode.MULTI:
            if run_in_thread:
                Thread(target=playable.play, daemon=True).start()
            else:
                playable.play()

    def _play_and_seek(self, playable, start, end):
        player = playable.play()

        player.seek(start / 1000)
        player.play()

        time.sleep(end / 1000)

        player.delete()
