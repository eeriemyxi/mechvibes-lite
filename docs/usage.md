# Usage
This page is a guide to using Mechvibes Lite from the command-line. 

!!! important 
    Please ensure you have the software installed by following the
    instructions [here](/#installation).

## Running Mechvibes Lite
```shell
mvibes daemon
```
This will start Mechvibes Lite on your computer.

!!! important 
    Please ensure you have a proper configuration file beforehand by
    following the instructions [here](#configuration).

!!! tip 
    A [Wskey](#wskey) server is automatically ran in the background for you unless it
    is told otherwise.

### Wskey
Wskey is included in the standard installation of Mechvibes Lite. It is a
background process that tells Mechvibes Lite which keys you are pressing. That
lets the main program know when to play which sound file. More advanced
introduction below.

Wskey under the hood is just a WebSocket server. You can start this daemon
yourself by doing the following:

```shell
mvibes wskey daemon
```

Wskey daemon on Linux depends on the `evdev` package from Pypi repositories. For
Windows it depends on `keyboard` package from the same repository.

!!! warning
    As of now, the connection is fully un-encrypted. The only information
    the daemon sends are the scan codes. Unless a malicious program is
    specifically targeting Mechvibes Lite users, it should be plentifully
    obscure what the server is actually sending. However encrypted connection
    may be introduced in a future release.

The host address and the port is first fetched from `wskey` key in the
configuration file. More information is available [here](#configuration).
However the subcommand has a number of flags to override the configuration file:

```shell
mvibes wskey daemon --host localhost --port 8765 --event-id 18
```

Additionally the main `daemon` subcommand also has `--wskey-port` and
`--wskey-host` flags to specify which server to connect to.
