import os
import pathlib
import sys


def get_config_path(app_name: str) -> pathlib.Path:
    """Get a cross-platform configuration directory for the given application.

    Args:
        app_name (str): The name of the application.

    Returns:
        pathlib.Path: The path to the configuration directory.

    """
    if os.name == "nt":  # Windows
        config_dir = os.getenv("APPDATA", pathlib.Path.home() / "AppData" / "Roaming")
    elif os.name == "posix":
        if sys.platform == "darwin":  # macOS
            config_dir = pathlib.Path.home() / "Library" / "Application Support"
        else:  # Linux and other Unix-like systems
            config_dir = pathlib.Path(
                os.getenv("XDG_CONFIG_HOME", pathlib.Path.home() / ".config")
            )
    else:
        raise RuntimeError("Unsupported platform")

    return config_dir / app_name
