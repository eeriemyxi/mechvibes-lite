import asyncio
import logging

from websockets.asyncio.server import serve

from mechvibes_lite import const

log = logging.getLogger(__name__)

logging.getLogger("websockets").setLevel(logging.INFO)


async def keyboard_mod_sender(websocket) -> None:
    log.debug("Sending keys from keyboard_mod_sender")
    import keyboard

    while True:
        event = keyboard.read_event()
        log.debug("Got event: %s", event)

        if event.event_type is not keyboard.KEY_UP:
            continue

        log.debug("Sending scancode from event: %s", event)

        await websocket.send(str(event.scan_code))


async def evdev_sender(websocket) -> None:
    log.debug("Sending keys from evdev_sender")
    import evdev

    device = evdev.InputDevice(const.EVENT_PATH)

    await websocket.send(str(1))

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
    if sys.platform == "win32":
        return keyboard_mod_sender
    raise NotImplementedError(f"No listener for {sys.platform} yet")


async def start() -> None:
    host = const.WSKEY_HOST
    port = const.WSKEY_PORT

    sender = get_appropriate_sender()

    server = await serve(sender, host, port)
    await server.serve_forever()
