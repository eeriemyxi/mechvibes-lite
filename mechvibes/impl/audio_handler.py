from __future__ import annotations

import contextlib
import typing as t
from functools import partial
from threading import Thread

import pyglet.clock  # type: ignore
import pyglet.media  # type: ignore

from mechvibes.impl import constants

if t.TYPE_CHECKING:
    from mechvibes.impl.parser import ConfigParser


class AudioHandler:
    def __init__(self, parser: ConfigParser):
        self.parser = parser
        self.addressed_audio_indices = {
            item.scancode: item for item in self.parser.iter_audio_indices()
        }
        self.sfx_pack_source = self.get_sfx_pack_source()

    def get_sfx_pack_source(self) -> pyglet.media.Source | None:
        if self.parser.audio_mode == constants.ThemeAudioMode.SINGLE:
            return pyglet.media.load(str(self.parser.sfx_pack_path), streaming=False)  # type: ignore
        return None

    def play(
        self,
        playable: pyglet.media.Source,
        *,
        timeline: tuple[int, int] | None = None,
        run_in_thread: bool = False,
    ) -> None:
        if timeline and self.parser.audio_mode == constants.ThemeAudioMode.SINGLE:
            player = pyglet.media.Player()
            player.queue(playable)  # type: ignore
            if run_in_thread:
                thread = Thread(
                    target=self._seek_and_play,
                    args=(player, *timeline),
                    daemon=True,
                )
                thread.start()
            else:
                self._seek_and_play(player, *timeline)
        elif self.parser.audio_mode == constants.ThemeAudioMode.MULTI:
            if run_in_thread:
                Thread(target=playable.play, daemon=True).start()
            else:
                playable.play()

    def _seek_and_play(self, player: pyglet.media.Player, start: int, end: int) -> None:
        player.seek(start / 1000)  # type: ignore
        player.play()
        pyglet.clock.schedule_once(partial(self._end_player, player), end / 1000)  # type: ignore

    @staticmethod
    def _end_player(player: pyglet.media.Player, _: float) -> None:
        with contextlib.suppress(TypeError):
            player.delete()
