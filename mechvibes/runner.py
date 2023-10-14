from mechvibes.impl.constants import PLATFORM
from mechvibes.impl.core import App


def run():
    app = App()

    app.run(platform=PLATFORM)
