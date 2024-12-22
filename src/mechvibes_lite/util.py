import os
import pathlib
import sys


def get_config_path(app_name: str) -> pathlib.Path:
    if os.name == "nt":
        config_dir = os.getenv("APPDATA", pathlib.Path.home() / "AppData" / "Roaming")
    elif os.name == "posix":
        if sys.platform == "darwin":
            config_dir = pathlib.Path.home() / "Library" / "Application Support"
        else:
            sys_config_dir = pathlib.Path("/etc") / app_name
            if sys_config_dir:
                return sys_config_dir

            config_dir = pathlib.Path(
                os.getenv("XDG_CONFIG_HOME", pathlib.Path.home() / ".config")
            )
    else:
        raise RuntimeError("Unsupported platform")

    return config_dir / app_name


def parse_event_id(event_id):
    if event_id.isdigit():
        event_id = f"event{event_id}"
    return event_id


def default_logging_config(log_level):
    return dict(
        level=log_level.upper(),
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )