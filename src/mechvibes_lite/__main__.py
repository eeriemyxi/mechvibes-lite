import asyncio
import pathlib
import argparse
import logging
import threading

import pyglet.app
import pyglet.media
from websockets.asyncio.client import connect

from mechvibes_lite import audio, const, struct, util
from mechvibes_lite.wskey.__main__ import parser as wskey_parser

LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)


async def daemon(theme_path, wskey_host, wskey_port) -> None:
    theme = struct.Theme.from_config(theme_path / "config.json", theme_path)
    keyplayer = audio.KeyPlayer(theme)

    async for websocket in connect(f"ws://{wskey_host}:{wskey_port}", ping_timeout=None):
        try:
            async for message in websocket:
                code = int(message)
                log.debug("Received scan code: %s", code)
                keyplayer.play_for(int(code))
        except websockets.exceptions.ConnectionClosed:
            log.warning("Connection to wskey was lost.")
            continue


def cmd_daemon(args) -> None:
    if args.theme_dir:
        const.THEME_DIR = args.theme_dir
    if args.theme_folder_name:
        const.THEME_FOLDER_NAME = args.theme_folder_name
        const.THEME_PATH = const.THEME_DIR / const.THEME_FOLDER_NAME
    pyglet.options["headless"] = True
    thread = threading.Thread(target=asyncio.run, args=[daemon(const.THEME_PATH, args.wskey_host, args.wskey_port)], daemon=True)
    thread.start()
    pyglet.app.run()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-L",
        "--log-level",
        help="Set log level. Options: DEBUG, INFO (default), CRITICAL, ERROR",
        type=str,
        default="INFO",
    )
    subparsers = parser.add_subparsers()

    subparsers.add_parser(
        "wskey", parents=[wskey_parser], conflict_handler="resolve"
    )

    subparser_daemon = subparsers.add_parser("daemon")
    subparser_daemon.add_argument("--wskey-host", default=const.WSKEY_HOST)
    subparser_daemon.add_argument("--wskey-port", default=const.WSKEY_PORT)
    subparser_daemon.add_argument("--theme-dir", default=const.THEME_DIR, type=pathlib.Path)
    subparser_daemon.add_argument("--theme-folder-name", default=const.THEME_FOLDER_NAME, type=pathlib.Path)
    subparser_daemon.set_defaults(func=cmd_daemon)

    args = parser.parse_args()

    LOG_LEVEL = args.log_level
    logging.basicConfig(**util.default_logging_config(LOG_LEVEL))

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    args.func(args)

    pyglet.app.run()


if __name__ == "__main__":
    main()
