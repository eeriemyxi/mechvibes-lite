import argparse
import asyncio
import logging
import pathlib
import sys
import threading

import pyglet.app
import pyglet.media
import websockets.exceptions
from websockets.asyncio.client import connect

from mechvibes_lite import audio, const, struct, util, wskey

log = logging.getLogger(__name__)


async def start_wskey_listener(theme_path, wskey_host, wskey_port) -> None:
    theme = struct.Theme.from_config(theme_path / "config.json", theme_path)
    keyplayer = audio.KeyPlayer(theme)

    async for websocket in connect(
        f"ws://{wskey_host}:{wskey_port}", ping_timeout=None
    ):
        try:
            async for message in websocket:
                code = int(message)
                log.debug("Received scan code: %s", code)
                keyplayer.play_for(int(code))
        except websockets.exceptions.ConnectionClosed:
            log.warning("Connection to wskey was lost.")
            continue


def ensure_required_flags(args) -> None:
    required_flags = ["theme_dir", "theme_folder_name", "wskey_host", "wskey_port"]
    if sys.platform == "linux":
        required_flags.append("event_id")
    for flag in required_flags:
        if not getattr(args, flag, None):
            raise ValueError(
                f"'--{util.to_kebab(flag)}' flag was expected but not provided."
            )


def cmd_wskey_daemon(host, port, event_id=None) -> None:
    try:
        asyncio.run(wskey.start(host, port, event_id))
    except KeyboardInterrupt:
        log.info("Closing wskey...")
        sys.exit()


def cmd_daemon(theme_path, wskey_host, wskey_port) -> None:
    pyglet.options["headless"] = True
    thread = threading.Thread(
        target=asyncio.run,
        args=[start_wskey_listener(theme_path, wskey_host, wskey_port)],
        daemon=True,
    )
    thread.start()
    pyglet.app.run()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mechvibes Lite is an alternative to Mechvibes "
        "(it plays sounds when you press keys)."
    )
    parser.add_argument(
        "-L",
        "--log-level",
        help="Set log level. Options: DEBUG, INFO (default), CRITICAL, ERROR",
        type=str,
        default="INFO",
    )
    parser.add_argument(
        "--no-config",
        help="Don't read config file from standard locations. "
        "Will error if you don't provide required configuration as flags instead.",
        action="store_true",
    )
    parser.add_argument(
        "--with-config",
        help="Load this configuration instead of the one at the standard location. "
        "Can be - for stdin.",
        type=argparse.FileType("r"),
    )
    parser.add_argument("--theme-dir")
    parser.add_argument("--theme-folder-name")
    parser.add_argument(
        "--wskey-host",
    )
    parser.add_argument(
        "--wskey-port",
    )

    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    subparser_daemon = subparsers.add_parser(
        "daemon", help="Run the keyboard input player as a daemon"
    )
    subparser_daemon.set_defaults(func=cmd_daemon)

    subparser_wskey = subparsers.add_parser(
        "wskey", help="WebSocket server for sending keyboard input"
    )

    wskey_subparsers = subparser_wskey.add_subparsers(dest="wskey", required=True)

    # [FIXME] --host and --port pollutes the global namespace;
    #         figure out something to have nested namespaces.
    wskey_subparser_daemon = wskey_subparsers.add_parser(
        "daemon", help="Run the server as a daemon"
    )
    wskey_subparser_daemon.add_argument("--host")
    wskey_subparser_daemon.add_argument("--port")
    wskey_subparser_daemon.add_argument("--event-id")
    wskey_subparser_daemon.set_defaults(func=cmd_wskey_daemon)

    args = parser.parse_args()

    LOG_LEVEL = args.log_level
    logging.basicConfig(**util.default_logging_config(LOG_LEVEL))

    if args.with_config:
        config = struct.Configuration.from_config(args.with_config.read())

    if args.no_config:
        try:
            ensure_required_flags(args)
        except ValueError as e:
            # [INFO] args[0] is basically the error message
            log.error(e.args[0])
            exit(1)
        try:
            config = struct.Configuration(
                args.theme_dir,
                args.theme_folder_name,
                args.wskey_host,
                args.wskey_port,
                event_id=args.event_id,
            )
        except (KeyError, FileNotFoundError) as e:
            log.error(e.args[0])
            exit(1)

    if not args.with_config and not args.no_config:
        config_home = util.get_config_path(const.APP_NAME)
        config_path = config_home / "config.ini"

        if not config_home.exists():
            log.error("Configuration directory not found at '%s'", config_home)
            exit(1)
        if not config_path.exists():
            log.error("'config.ini' not found at '%s'", config_path)
            exit(1)

        config = struct.Configuration.from_config(config_path.read_text())

        if args.theme_dir:
            config.theme_dir = pathlib.Path(args.theme_dir).expanduser().resolve()
        if args.theme_folder_name:
            config.theme_folder_name = args.theme_folder_name
            config.theme_path = config.theme_dir / config.theme_folder_name
        if args.wskey_host:
            config.wskey_host = args.wskey_host
        if args.wskey_port:
            config.wskey_port = args.wskey_port
        if args.event_id:
            config.event_id = util.parse_event_id(args.event_id)
            config.event_path = config.event_path_base / config.event_id
    if args.subcommand == "wskey":
        args.func(
            args.host or config.wskey_host,
            args.port or config.wskey_port,
            config.event_path,
        )
    elif args.subcommand == "daemon":
        args.func(config.theme_path, config.wskey_host, config.wskey_port)

    pyglet.app.run()


if __name__ == "__main__":
    main()
