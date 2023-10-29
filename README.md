# Introduction
This is a lightweight CLI-based version of
[Mechvibes](https://github.com/hainguyents13/mechvibes). No Electron.
Only supports Linux and Windows. (See [why](../../wiki#others)).
## Features
* Full support for themes made for the original [Mechvibes](https://github.com/hainguyents13/mechvibes).
* Easy CLI interface.
  * `mvibes run` runs the app.
  * `mvibes run --with active_theme.id=eg-oreo` overrides the active
  theme specified in `configuration.yml`. You can override any option in the file
  using this option. You are allowed to use this option multiple times like this:
  `mvibes run --with key.subkey=vaue --with another_key.another_rub_key=value`.
  * See `mvibes --help` for more information.
* Default themes same as the original Mechvibes, see [themes](mechvibes/themes).

# Instructions to Install
See the [wiki page](../../wiki#installation) for instructions to install.

# Usage
See the [wiki page](../../wiki#usage) for a guide to using this project.

# Configuration
Configuration is done in the `configuration.yml` file. See the [wiki page](../../wiki#configuration) for documentation.

# Contributing
Thank you for your interest. Please see [CONTRIBUTING.md](CONTRIBUTING.md).

# License
This project is licensed under the [MIT license](LICENSE).
