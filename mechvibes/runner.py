from mechvibes.impl.constants import PLATFORM
from mechvibes.impl.core import App


def run(event_code=None):
    app = App()

    if event_code:
        event_code = int(event_code)

    app.run(platform=PLATFORM, event_code=event_code)
