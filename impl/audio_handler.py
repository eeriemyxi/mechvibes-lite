from impl import constants


class AudioHandler:
    def __init__(self, parser):
        self.parser

    def play(self, player, *, timeline: tuple[int, int] | None=None, run_in_thread: bool=False):
        ...
