import kisesi
import pathlib
from functools import partial

import pyglet.clock
import pyglet.media as media

from mechvibes_lite import struct

log = kisesi.get_logger(__name__)


class SingleAudioKeyPlayer:
    def __init__(self, audio: pathlib.Path, defines: dict[int, tuple[int, int]]):
        self.audio = media.StaticSource(media.load(str(audio), streaming=False))
        self.defines = defines

    def _seek_and_play(self, player: media.Player, start: int, end: int) -> None:
        player.seek(start / 1000)
        player.play()
        pyglet.clock.schedule_once(partial(self._end_player, player), end / 1000)

    @staticmethod
    def _end_player(player: media.Player, _: float) -> None:
        player.pause()
        player.delete()

    def play_for(self, scan_code: int) -> None:
        log.debug(f"Playing for {scan_code=}")
        timeline = self.defines.get(scan_code)

        if not timeline:
            log.warn(
                f"Returning for {scan_code=} because I coudn't find an audio for it."
            )
            return

        player = media.Player()
        player.queue(self.audio)
        self._seek_and_play(player, *timeline)


class MultiAudioKeyPlayer:
    def __init__(self, base_path: pathlib.Path, defines: dict[int, str]):
        self.base_path = base_path
        self.defines = defines
        self.sources = self.get_sources(self.defines)

    def get_sources(self, defines: dict[int, str]):
        return {s: media.load(s, streaming=False) for s in set(defines.values())}

    def play_for(self, scan_code: int) -> None:
        log.debug(f"Playing for {scan_code=}")

        audio_src_path = self.defines.get(scan_code)
        log.debug(f"{audio_src_path=}")
        if not audio_src_path:
            log.warn(
                f"Returning for {scan_code=} because I coudn't find an audio for it."
            )
            return

        player = self.sources[audio_src_path]
        log.debug(f"{player=}")

        player.play()
        log.debug(f"Done playing for {scan_code=}")


class KeyPlayer:
    def __init__(self, theme: struct.Theme):
        self.theme = theme
        self.player = self.find_player_for(self.theme)

    def find_player_for(
        self, theme: struct.Theme
    ) -> SingleAudioKeyPlayer | MultiAudioKeyPlayer:
        if theme.type is struct.PlaybackType.SINGLE_FILE:
            return SingleAudioKeyPlayer(theme.sound, theme.defines)
        if theme.type is struct.PlaybackType.MULTI_FILE:
            return MultiAudioKeyPlayer(theme.base_path, theme.defines)
        return None

    def play_for(self, scan_code: int) -> None:
        self.player.play_for(scan_code)
