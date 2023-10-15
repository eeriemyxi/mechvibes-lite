from __future__ import annotations

import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from pathlib import Path

    from pyglet.media import Source


@dataclass
class DirectAudio:
    playable: Source
    path: Path
    scancode: int


@dataclass
class LocativeAudio:
    timeline: tuple[int, int]
    scancode: int
