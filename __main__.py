from impl.constants import PLATFORM
from impl.core import App

app = App()

app.run_pyglet_event_loop(PLATFORM)
