import logging
import sys
from functools import partial

from websockets.asyncio.server import serve

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


async def evdev_sender(websocket, *, event_path) -> None:
    log.debug("Sending keys from evdev_sender")
    import evdev

    device = evdev.InputDevice(event_path)

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


async def start(host, port, event_path=None) -> None:
    if sys.platform == "linux":
        if not event_path.exists():
            raise FileNotFoundError(
                f"event_path specified as '{event_path}' but it doesn't exist."
            )

        sender = partial(evdev_sender, event_path=event_path)
    elif sys.platform == "win32":
        sender = keyboard_mod_sender
    else:
        raise NotImplementedError(f"No listener for {sys.platform} yet")

    server = await serve(sender, host, port)
    await server.serve_forever()
