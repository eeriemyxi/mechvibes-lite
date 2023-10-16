from mechvibes.impl.core import App
from mechvibes.impl.constants import Platform


def run(platform: Platform):
    app = App()

    app.run(platform=platform)
