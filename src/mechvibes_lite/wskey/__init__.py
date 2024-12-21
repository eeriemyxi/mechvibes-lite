
import asyncio
import logging

from websockets.server import serve

from mechvibes_lite import const

log = logging.getLogger(__name__)


async def evdev_sender(websocket) -> None:
    import evdev

    device = evdev.InputDevice(const.EVENT_PATH)

    for event in device.read_loop():
        if event.type != evdev.ecodes.EV_KEY:
            continue

        key = evdev.categorize(event)
        log.debug("Got key: %s", key)

        if key.keystate != evdev.KeyEvent.key_down:
            continue

        log.debug("Sending key: %s", key)
        await websocket.send(str(key.scancode))


def get_appropriate_sender():
    import sys

    if sys.platform == "linux":
        return evdev_sender
    raise NotImplementedError(f"No listener for {sys.platform} yet")


async def start() -> None:
    host = const.WSKEY_HOST
    port = const.WSKEY_PORT

    sender = get_appropriate_sender()

    async with serve(sender, host, port):
        await asyncio.get_running_loop().create_future()
