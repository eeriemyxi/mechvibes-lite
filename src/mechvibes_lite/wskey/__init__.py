import asyncio
import sys
from functools import partial

import kisesi
from websockets.asyncio.server import serve

log = kisesi.get_logger(__name__)

kisesi.get_logger("websockets").set_level(kisesi.INFO)


async def keyboard_mod_sender(websocket) -> None:
    log.debug("Sending keys from keyboard_mod_sender")
    import keyboard

    loop = asyncio.get_running_loop()
    keys_down = []

    while True:
        try:
            event = await loop.run_in_executor(None, keyboard.read_event)
        except RuntimeError:
            await asyncio.sleep(0.1)
            continue

        log.debug("Got event: %s", event)

        if event.event_type is keyboard.KEY_UP:
            keys_down.remove(event.scan_code)
            continue

        if event.scan_code in keys_down or event.event_type is not keyboard.KEY_DOWN:
            continue

        keys_down.append(event.scan_code)

        log.debug(f"Sending {event.scan_code=} from {event=}")
        await websocket.send(str(event.scan_code))


async def evdev_sender(websocket, *, event_path) -> None:
    log.debug("Sending keys from evdev_sender")
    import evdev

    device = evdev.InputDevice(event_path)

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

    log.debug(f"Serving wskey on {host=} {port=}")
    server = await serve(sender, host, port)
    await server.serve_forever()
