# Source Generated with Decompyle++
# File: __main__.cpython-311.pyc (Python 3.11)

from impl.constants import PLATFORM
from impl.core import App

app = App()
app.instigate_listener(platform=PLATFORM, run_in_thread=True)
app.run_pyglet_event_loop()
