import importlib
import json
import logging
import os
import typing as t

import click
import mergedeep  # type: ignore
from typing_extensions import Unpack

from mechvibes.cli.struct import ConfigDefinition
from mechvibes.cli.utils import parse_config_address
from mechvibes.impl import constants
from mechvibes.runner import run as run_mechvibes

logger = logging.getLogger(__name__)

CONFIG_DEFINITION_TYPE = ConfigDefinition()
RunSubcommandKwargs = t.TypedDict(
    "RunSubcommandKwargs", {"with": list[tuple[str, str]]}
)


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("--with", "-w", multiple=True, type=CONFIG_DEFINITION_TYPE)
def run(**kwargs: Unpack[RunSubcommandKwargs]) -> None:
    logger.info("Loading configurations...")

    if kwargs["with"]:
        base_conf_ovr = parse_config_address(*kwargs["with"][0])

        for conf_ovr in kwargs["with"][1:]:
            mergedeep.merge(base_conf_ovr, parse_config_address(*conf_ovr))  # type: ignore

        os.environ["MECHVIBES_CONFIG_OVERWRITES"] = json.dumps(base_conf_ovr)

        logger.info("Configuration overwrites found. Reloading configuration...")
        importlib.reload(constants)

    run_mechvibes(constants.PLATFORM)
