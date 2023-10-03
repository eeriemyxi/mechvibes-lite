import functools
import json
import os
import os.path
import sys
import time
from threading import Thread

import pyglet.app
import pyglet.media

if sys.platform == "win32":
    import keyboard
elif sys.platform == "linux":
    import evdev
    try:
        EVENT = int(sys.argv[1])
    except IndexError:
        raise Exception("(Linux) You are expected to pass the device event number as a command line argument.")

with open(
    os.path.join(sys.path[0], "active_config/config.json"), "r"
) as config_file_buffer:
    CONFIG = json.load(config_file_buffer)

keyboard_states = {}

MODE = CONFIG["key_define_type"]
if MODE == "multi":
    sfxes = os.listdir("active_config")
    sfxes.remove("config.json")
    db = {}
    for fx in sfxes:
        path = os.path.join(sys.path[0], f"active_config/{fx}")
        db[fx] = pyglet.media.load(
                path, streaming=False
            )
else:
    db = {k: tuple(v) for k, v in (i for i in CONFIG["defines"].items() if i[1])}
    filename = CONFIG["sound"]
    sound_source = pyglet.media.load(
        os.path.join(sys.path[0], f"active_config/{filename}"), streaming=False
    )

print("Now monitoring for keyboard events. Please try pressing keys.")


def handler_windows_on_hook(keyboard_states, event):
    key_code = event.scan_code
    keyboard_states[key_code] = event.event_type

    if key_code in keyboard_states and keyboard_states[key_code] == "down":
        return

    try:
        if MODE == "multi":
            Thread(
                target=db[CONFIG["defines"][str(key_code)]].play, daemon=True
            ).start()
        else:
            timers = db[str(key_code)]
            Thread(
                target=play_sfx,
                args=(player.play(), *timers),
                daemon=True,
            ).start()
    except KeyError:
        ...


def handler_linux_on_hook(event):
    if event.type == evdev.ecodes.EV_KEY:
        key = evdev.categorize(event)
        if key.keystate == 1:
            try:
                if MODE == "multi":
                    src = db[CONFIG["defines"][str(key.scancode)]]
                    src.volume = 5.0
                    src.play()
                else:
                    timers = db[str(key.scancode)]
                    Thread(target=play_sfx, args=(sound_source.play(), *timers), daemon=True).start()
            except KeyError:
                ...


def play_sfx(player, start, end, *, should_exit: bool=False):
    if (start, end) != (0, 0):
        player.seek(start / 1000)
        player.play()
        time.sleep(end / 1000)

    player.delete()

    if should_exit:
        sys.exit()


def main():
    if sys.platform == "win32":
        keyboard.hook(functools.partial(handler_windows_on_hook, keyboard_states))
    elif sys.platform == "linux":
        dev = evdev.InputDevice(f"/dev/input/event{EVENT}")

        for event in dev.read_loop():
            handler_linux_on_hook(event)

Thread(target=main, daemon=True).start()
pyglet.app.run()
