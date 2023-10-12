from impl.constants import PLATFORM
from impl.core import App

app = App()

app.instigate_listener(platform=PLATFORM, run_in_thread=True)
app.run_pyglet_event_loop()
