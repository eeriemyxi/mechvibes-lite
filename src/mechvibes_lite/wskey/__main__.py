import argparse
import asyncio
import logging
import sys

from mechvibes_lite import const, util, wskey

log = logging.getLogger(__name__)


def cmd_daemon(args) -> None:
    if args.host:
        const.WSKEY_HOST = args.host
    if args.port:
        const.WSKEY_PORT = args.port
    if args.event_id:
        const.EVENT_ID = util.parse_event_id(args.event_id)
        const.EVENT_PATH = const.EVENT_PATH_BASE / const.EVENT_ID

    try:
        asyncio.run(wskey.start())
    except KeyboardInterrupt:
        log.info("Closing wskey...")
        sys.exit()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

subparser_start = subparsers.add_parser("daemon")
subparser_start.add_argument("--host", default=const.WSKEY_HOST)
subparser_start.add_argument("--port", default=const.WSKEY_PORT)
subparser_start.add_argument("--event-id", default=const.EVENT_ID)
subparser_start.set_defaults(func=cmd_daemon)


def main() -> None:
    LOG_LEVEL = "INFO"
    parser.add_argument(
        "-L",
        "--log-level",
        help="Set log level. Options: DEBUG, INFO (default), CRITICAL, ERROR",
        type=str,
        default="INFO",
    )
    args = parser.parse_args()
    LOG_LEVEL = args.log_level

    logging.basicConfig(**util.default_logging_config(LOG_LEVEL))

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
