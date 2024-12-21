import argparse
import asyncio
import logging

from mechvibes_lite import wskey

log = logging.getLogger(__name__)


def cmd_start(args) -> None:
    asyncio.run(wskey.start())


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

subparser_start = subparsers.add_parser("daemon")
subparser_start.set_defaults(func=cmd_start)


def main() -> None:
    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
