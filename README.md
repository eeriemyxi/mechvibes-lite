# Mechvibes Lite
Mechvibes Lite is a lightweight alternative to Mechvibes. It boasts full compatibility with the original version.

# Demo
https://github.com/user-attachments/assets/3af7e7d6-dff7-414d-9ffc-c311231450ac

> [!NOTE]
> You browser might be muting the embedded video's audio by default.

# [Documentation](https://mechvibes-lite.pages.dev/)
Please visit <https://mechvibes-lite.pages.dev/> for documentation.

# [Installation](https://mechvibes-lite.pages.dev/#installation)
* [Documentation for Windows](https://mechvibes-lite.pages.dev/installation/windows/)
* [Documentation for Linux](https://mechvibes-lite.pages.dev/installation/linux/)

# [Configuration](https://mechvibes-lite.pages.dev/configuration/)
You can learn how to use this software
[here](https://mechvibes-lite.pages.dev/configuration/).

# [Usage](https://mechvibes-lite.pages.dev/usage/)
You need to setup a configuration file to use Mechvibes Lite. Instructions and
guidance can be found [here](https://mechvibes-lite.pages.dev/usage/).

# Command-line Arguments
```
usage: mvibes [-h] [-L LOG_LEVEL] [--no-config] [--with-config WITH_CONFIG]
              [--theme-dir THEME_DIR] [--theme-folder-name THEME_FOLDER_NAME]
              [--wskey-host WSKEY_HOST] [--wskey-port WSKEY_PORT] [--no-wskey]
              [--version]
              {daemon,wskey} ...

Mechvibes Lite is an alternative to Mechvibes (it plays sounds when you press
keys).

positional arguments:
  {daemon,wskey}
    daemon              Run the keyboard input player as a daemon
    wskey               WebSocket server for sending keyboard input

options:
  -h, --help            show this help message and exit
  -L LOG_LEVEL, --log-level LOG_LEVEL
                        Set log level. Options: DEBUG, INFO (default),
                        CRITICAL, ERROR
  --no-config           Don't read config file from standard locations. Will
                        error if you don't provide required configuration as
                        flags instead.
  --with-config WITH_CONFIG
                        Load this configuration instead of the one at the
                        standard location. Can be - for stdin.
  --theme-dir THEME_DIR
  --theme-folder-name THEME_FOLDER_NAME
  --wskey-host WSKEY_HOST
  --wskey-port WSKEY_PORT
  --no-wskey
  --version, -V         show program's version number and exit
```
