import logging

from mechvibes.impl.constants import Platform
from mechvibes.impl.core import App

logger = logging.getLogger(__name__)


def run(platform: Platform) -> None:
    logger.info("Starting the program...")

    app = App()

    app.run(platform=platform)
