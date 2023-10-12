import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from pathlib import Path

    from pyglet.media import Source


@dataclass
class DirectAudio:
    playable: Source
    path: Path
    keycode: int


@dataclass
class LocativeAudio:
    playable: Source
    timeline: (int, int)
    keycode: int
