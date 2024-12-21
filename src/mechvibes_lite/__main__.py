import argparse
import logging
import threading

import pyglet.app
import pyglet.media
from websockets.sync.client import connect

from mechvibes_lite import audio, const, struct
from mechvibes_lite.wskey.__main__ import parser as wskey_parser

log = logging.getLogger(__name__)


def daemon() -> None:
    theme = struct.Theme.from_config(const.THEME_PATH / "config.json", const.THEME_PATH)
    keyplayer = audio.KeyPlayer(theme)

    with connect(f"ws://{const.WSKEY_HOST}:{const.WSKEY_PORT}") as websock:
        while True:
            code = websock.recv()
            log.debug("Received scan code: %s", code)
            keyplayer.play_for(int(code))


def cmd_daemon(args) -> None:
    pyglet.options["headless"] = True
    thread = threading.Thread(target=daemon, daemon=True)
    thread.start()
    pyglet.app.run()


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    _ = subparsers.add_parser(
        "wskey", parents=[wskey_parser], conflict_handler="resolve"
    )

    subparser_daemon = subparsers.add_parser("daemon")
    subparser_daemon.set_defaults(func=cmd_daemon)

    args = parser.parse_args()
    args.func(args)

    pyglet.app.run()


if __name__ == "__main__":
    main()
