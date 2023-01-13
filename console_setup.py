import ctypes
import os
import sys

TITLE = "Mechvibes Lite"


def set_title():
    if sys.platform == "linux":
        sys.stdout.write(f"\x1b]2;{TITLE}\x07")
    elif sys.platform == "win32":
        ctypes.windll.kernel32.SetConsoleTitleW(TITLE)


def clear_screen():
    os.system("cls||clear")
