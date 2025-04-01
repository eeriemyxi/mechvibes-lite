import asyncio
import importlib.metadata
import pathlib
import sys
import threading

import click
import kisesi
import websockets

from mechvibes_lite import const, struct, util, wskey

kisesi.basic_config(level="INFO")
log = kisesi.get_logger(__name__)


async def start_wskey_listener(theme_path, wskey_host, wskey_port) -> None:
    from mechvibes_lite import audio

    log.debug(f"Started wskey listener {wskey_host=} {wskey_port=}")
    theme = struct.Theme.from_config(theme_path / "config.json", theme_path)
    keyplayer = audio.KeyPlayer(theme)

    async for websocket in websockets.connect(
        f"ws://{wskey_host}:{wskey_port}", ping_timeout=None
    ):
        try:
            log.debug("Got a connection...")
            async for message in websocket:
                code = int(message)
                log.debug("Received scan code: %s", code)
                keyplayer.play_for(int(code))
        except websockets.exceptions.ConnectionClosed:
            log.warning("Connection to wskey was lost.")
            continue


def ensure_required_flags(args) -> bool:
    required_flags = ["theme_dir", "theme_folder_name", "wskey_host", "wskey_port"]
    if sys.platform == "linux":
        required_flags.append("event_id")

    for flag in required_flags:
        if not args[flag]:
            log.error(f"'--{util.to_kebab(flag)}' flag was expected but not provided.")
            return False

    return True


@click.group(help=const.APP_DESCRIPTION, epilog=const.APP_EPILOG)
@click.option(
    "--log-level",
    "-L",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]),
    default="INFO",
)
@click.option(
    "--no-config",
    help="Do not read config file from standard locations. "
    "Will error if you don't provide required configuration as flags instead.",
    is_flag=True,
    default=False,
)
@click.option(
    "--no-wskey", help="Do not run the Wskey daemon.", is_flag=True, default=False
)
@click.option(
    "--with-config",
    help="Load this configuration instead of the one at the standard location. Can be - for stdin.",
    type=click.File("r"),
    default=None,
)
@click.option(
    "--theme-dir",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Path to the theme directory.",
    default=None,
)
@click.option(
    "--theme-folder-name",
    help="Name of the theme folder. This folder must exist under --theme-dir.",
    default=None,
)
@click.option(
    "--wskey-host",
    help="The hostname to use to connect to the Wskey daemon.",
    default=None,
)
@click.option(
    "--wskey-port",
    type=int,
    help="The port to use to connect to the Wskey daemon.",
    default=None,
)
@click.option(
    "--event-id",
    help="The port to use for the Wskey server started when --no-wskey is *not* provided.",
    default=None,
)
@click.version_option(
    version=importlib.metadata.version(const.APP_NAME),
    prog_name=const.APP_NAME.replace("-", " ").title(),
)
@click.pass_context
def cli(
    ctx,
    log_level: str,
    no_config: bool,
    no_wskey: bool,
    with_config: str,
    theme_dir: pathlib.Path,
    theme_folder_name: str,
    wskey_host: str,
    wskey_port: int,
    event_id: str,
):
    log.set_level(log_level)

    ctx.config = None

    if no_config and not with_config:
        ret = ensure_required_flags(ctx.params)
        if not ret:
            sys.exit(1)
        ctx.config = struct.Configuration(
            theme_dir, theme_folder_name, wskey_host, wskey_port
        )
        log.debug(
            f"[NO_CONFIG, NO_WITH_CONFIG] Constructed {ctx.config} since {no_config=} and {with_config=}"
        )
    elif with_config:
        ctx.config = struct.Configuration.from_config(with_config.read())
        log.debug(
            f"[WITH_CONFIG] Constructed {ctx.config} since {no_config=} and {with_config=}"
        )
    else:
        ctx.config = struct.Configuration.from_config(const.CONFIG_PATH.read_text())
        log.debug(
            f"Constructed {ctx.config} from {const.CONFIG_PATH=} since {no_config=} and {with_config=}"
        )

    if theme_dir:
        log.debug(f"Setting {ctx.config.theme_dir=} to {theme_dir=}")
        ctx.config.theme_dir = theme_dir
    if theme_folder_name:
        log.debug(f"Setting {ctx.config.theme_folder_name=} to {theme_folder_name=}")
        ctx.config.theme_folder_name = theme_folder_name
    if wskey_host:
        log.debug(f"Setting {ctx.config.wskey_host=} to {wskey_host=}")
        ctx.config.wskey_host = wskey_host
    if wskey_port:
        log.debug(f"Setting {ctx.config.wskey_port=} to {wskey_port=}")
        ctx.config.wskey_port = wskey_port
    if event_id:
        if sys.platform != "linux":
            log.error("--event-id flag is only for Linux users.")
            sys.exit(1)
        log.debug(f"Setting {ctx.config.event_id=} to {event_id=}")
        ctx.config.event_id = util.parse_event_id(event_id)

    log.debug(f"Finalised configuration: {ctx.config=}")


@cli.command(name="daemon", help="Run the keyboard input player as a daemon.")
@click.pass_context
def mvibes_daemon(ctx):
    root_ctx = ctx.find_root()
    config = root_ctx.config

    if not root_ctx.params["no_wskey"]:
        # [INFO] I don't know why I didn't use asyncio tasks instead.
        # And I am too scared to find out why.
        thread = threading.Thread(
            target=asyncio.run,
            args=[wskey.start(config.wskey_host, config.wskey_port, config.event_path)],
            daemon=True,
        )
        thread.start()

    import pyglet.app
    import pyglet.media

    log.debug("Starting daemon")
    pyglet.options["headless"] = True
    thread = threading.Thread(
        target=asyncio.run,
        args=[start_wskey_listener(config.theme_path, config.wskey_host, config.wskey_port)],
        daemon=True,
    )
    thread.start()

    try:
        pyglet.app.run()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        log.info(f"Exiting {const.APP_NAME}...")
        sys.exit()


@cli.group(help="WebSocket server for sending keyboard input.", name="wskey")
@click.option("--host", help="The hostname for the Wskey daemon.", default=None)
@click.option("--port", type=int, help="The port for the Wskey daemon.", default=None)
@click.option(
    "--event-id", help="The event id to use for the Wskey daemon.", default=None
)
def cmd_wskey(host: str, port: int, event_id: str):
    if event_id and sys.platform != "linux":
        log.error("--event-id flag is only for Linux users.")
        sys.exit(1)


@cmd_wskey.command(name="daemon", help="Run a Wskey daemon.")
@click.pass_context
def wskey_daemon(ctx):
    params = ctx.parent.params
    config = ctx.find_root().config
    event_id = params["event_id"]
    
    host = params["host"] or config.wskey_host
    port = params["port"] or config.wskey_port
    event_path = util.parse_event_id(event_id) if event_id else config.event_path

    try:
        asyncio.run(wskey.start(host, port, event_path))
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        log.info("Closing wskey...")
        sys.exit()


if __name__ == "__main__":
    main()
