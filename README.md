# Note
This is a rough implementation with very limited functionality.

# Introduction
Mechvibes Lite is a CLI version of [Mechvibes](https://github.com/hainguyents13/mechvibes), focused on lower memory usage. It doesn't make use of Electron for as basic program as this; I tend to believe that Electron is meant for much more bigger projects. As of now, I have only tested it on Windows, but the libraries I have used should be cross-platform. I have a few crucial tasks to be done, once those are finished, I will work on this project to try to minimise the memory usage further, and to make it much functionable and object-oriented.

# How to Use
If you want to use a default configuration provided by Mechvibes, go to the `default_configs` folder, pick your configuration, open the folder, copy the files to `active_config` (after deleting all the files in the `active_config` folder).

# Known Issues
- Its sound player is not as powerful as of a whole goddamn Chromium browser, so try to use popular audio formats. I observed that creators of some configurations in the Discord server of Mechvibes merely rename video files as audio files which works well for the Electron app, but won't on this one. In the future there will be a pretty and elegant configuration chooser and auto-conversion of files using FFMPEG.
- Due to unknown reasons, on initialization of the program, it will use ~55MB RAM but eventually this will drop to less than 25 MB (depends on various things including the audio files of the config; those are loaded in RAM). I will work on this later.
