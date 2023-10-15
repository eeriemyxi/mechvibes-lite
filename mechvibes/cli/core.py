import importlib
import json
import os

import click
import mergedeep

from mechvibes.cli.struct import ConfigDefinition
from mechvibes.cli.utils import parse_config_address
from mechvibes.impl import constants
from mechvibes.runner import run as run_mechvibes

CONFIG_DEFINITION = ConfigDefinition()


@click.group()
def main():
    pass


@main.command()
@click.option("--with", "-w", multiple=True, type=CONFIG_DEFINITION)
def run(**kwargs):
    if kwargs["with"]:
        base_conf_ovr = parse_config_address(*kwargs["with"][0])

        for conf_ovr in kwargs["with"][1:]:
            mergedeep.merge(base_conf_ovr, parse_config_address(*conf_ovr))
    else:
        base_conf_ovr = {}

    os.environ["MECHVIBES_CONFIG_OVERWRITES"] = json.dumps(base_conf_ovr)
    importlib.reload(constants)

    run_mechvibes(constants.PLATFORM)