# Configuring Mechvibes Lite
!!! important 
    Please ensure you have the software installed by following the
    instructions [here](index.md#installation).

## Example Configuration File
```ini
[general]
theme_dir = ~/.config/mechvibes-lite/themes
event_id = 17

[wskey]
host = localhost
port = 6969

[theme]
folder_name = nk-cream
```
This software uses `.ini` format for configuration.

!!! tip
    A reference for INI files can be found [here](https://quickref.me/ini.html).

!!! note 
    The `~` symbol in the `theme_dir`'s value is a shortcut to writing
    `/home/username` on Linux and on Windows, `C:/Users/username`. `username` in
    this context is the name of the logged in user's account name.

## Storing the Configuration File
On Linux, system-wide configuration can be stored at
`/etc/mechvibes-lite/config.ini`. User-wide configuration can be stored at
`~/.config/mechvibes-lite/config.ini`. `XDG_CONFIG_HOME` environment variable is
also respected.

On Windows, configuration file can be stored at
`%APPDATA%/mechvibes-lite/config.ini`. `%APPDATA` is an environment variable
that is typically expanded to `C:/Users/username/AppData/Roaming`. This might
refer to something else in special cases, it's best to check it by doing `echo
%APPDATA%` in Command Prompt or some other shell.

## Specifying Arbitrary Location for Configuration File
`--with-config` flag can be used to load a configuration from non-standard
location. You may put `-` to read standard input buffer. Example: `mvibes
--with-config /tmp/my-config.ini`, or `cat /tmp/my-config.ini | mvibes
--with-config -`.

`--no-config` flag can be used to _not_ load a configuration file. Instead
configuration may be entirely constructed with CLI flags, such as `--theme-dir`,
`--theme-folder-name`, etc. It's best to do `mvibes --help` for more
information.

## Overriding Configuration Options
There are various CLI flags to override the configuration file, such as
`--theme-dir`, `--theme-folder-name`, etc. Please do `mvibes --help` for more
information.

## Description of the Options
| Key Name | Description |
|---|---|
| `theme.folder_name` | The name of the theme folder that Mvibes is supposed to play. |
| `theme.theme_dir` | A string that points to an _existing_ directory where themes compatible with original Mechvibes are available. |
| `wskey.host` | The hostname of the Wskey server. |
| `wskey.port` | The port of the Wskey server.  |
| `wskey.event_id`  | Only applicable for Linux. The ID of the input event to listen to. If the string is an integer then it is converted to `event{id}` where `id` is the integer.|

## In-depth Description
To understand `wskey.*` options, it is recommended to refer to documentation
available [here](usage.md#wskey).

To undersand `wskey.event_id`, you should refer to documentation available
[here](installation/linux.md#testing-access-for-input-event).
