from os import get_terminal_size, listdir, path

from rich import print
from rich.console import Console
console = Console()

import console_setup

console_setup.clear_screen()
print("\n" * (get_terminal_size().lines // 2 - 1))
console.print("[yellow][ LOADING... ][/yellow]", justify="center")

from json import load as load_json
from random import choice as pick_one_randomly
import sys
from threading import Thread
from time import sleep, time

import pyglet.app
import pyglet.media

import keyboard


with open(path.join(sys.path[0], "active_config/config.json"), "r") as config_file_buffer:
    CONFIG = load_json(config_file_buffer)

keyboard_states = {}
fixes = {"alt gr": "56", "left windows": "3675", "menu": "3613"}
closed = False

MODE = CONFIG["key_define_type"]
if MODE == "multi":
    sfxes = listdir("pack")
    sfxes.remove("config.json")
    db = {i: pyglet.media.load(path.join(sys.path[0], f"active_config/{i}"), streaming=False) for i in sfxes}
else:
    db = {k: tuple(v) for k, v in (i for i in CONFIG["defines"].items() if i[1])}
    filename = CONFIG["sound"]
    player = pyglet.media.load(path.join(sys.path[0], f"active_config/{filename}"), streaming=False)

console_setup.set_title()


def print_started():
    size = None
    while True:
        sleep(1)

        if closed:
            exit()
        if size and size == get_terminal_size().lines // 2 - 1:
            continue
        else:
            size = get_terminal_size().lines // 2 - 1

        console_setup.clear_screen()
        print("\n" * size)
        console.print("[green][ STARTED ][/green]", justify="center")
        print("\n" * (size - 1))

console.bell()
Thread(target=print_started).start()


def on_hook(event):
    key_code = event.scan_code

    keyboard_states = globals()["keyboard_states"]
    if key_code in keyboard_states and keyboard_states[key_code] == "down":
        keyboard_states[key_code] = event.event_type
        return
    keyboard_states[key_code] = event.event_type

    if MODE == "multi":
        try:
            Thread(target=db[CONFIG["defines"][str(key_code)]].play).start()
        except KeyError:
            Thread(target=db[CONFIG["defines"][fixes[event.name]]].play).start()
    else:
        try:
            timers = db[str(key_code)]
        except KeyError:
            timers = db[fixes[event.name]]
        Thread(
            target=play_sfx,
            args=(player.play(), *timers),
            daemon=True,
        ).start()


def play_sfx(player, start, end):
    if (start, end) != (0, 0):
        player.seek(start * 0.001)
        player.play()
        sleep(end * 0.001)
    player.volume = 0
    player.next_source()
    sys.exit()


keyboard.hook(on_hook)
try:
    pyglet.app.run()
except KeyboardInterrupt:
    closed = True
    console_setup.clear_screen()
    print("\n" * (get_terminal_size().lines // 2 - 1))
    console.print("[red][ CLOSING... ][/red]", justify="center")
    sys.exit()
