# Mechvibes Lite
Mechvibes Lite is a lightweight alternative to Mechvibes. It boasts full
compatibility with the original version.

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
You need to setup a configuration file to use Mechvibes Lite. Instructions and
guidance can be found [here](https://mechvibes-lite.pages.dev/configuration/).

# [Usage](https://mechvibes-lite.pages.dev/usage/)
You can learn how to use this software
[here](https://mechvibes-lite.pages.dev/usage/).

# Command-line Arguments
```
Usage: mvibes [OPTIONS] COMMAND [ARGS]...

  Mechvibes Lite is an alternative to Mechvibes (it plays sounds when you
  press keys.

Options:
  -L, --log-level [DEBUG|INFO|WARNING|CRITICAL|ERROR]
  --no-config                     Do not read config file from standard
                                  locations. Will error if you don't provide
                                  required configuration as flags instead.
  --no-wskey                      Do not run the Wskey daemon.
  --with-config FILENAME          Load this configuration instead of the one
                                  at the standard location. Can be - for
                                  stdin.
  --theme-dir PATH                Path to the theme directory.
  --theme-folder-name TEXT        Name of the theme folder. This folder must
                                  exist under --theme-dir.
  --wskey-host TEXT               The hostname to use to connect to the Wskey
                                  daemon.
  --wskey-port INTEGER            The port to use to connect to the Wskey
                                  daemon.
  --event-id TEXT                 The port to use for the Wskey server started
                                  when --no-wskey is *not* provided.
  --version                       Show the version and exit.
  --help                          Show this message and exit.

Commands:
  daemon  Run the keyboard input player as a daemon.
  wskey   WebSocket server for sending keyboard input.

  * Homepage for Mechvibes Lite is hosted at
  https://github.com/eeriemyxi/mechvibes-lite
```
