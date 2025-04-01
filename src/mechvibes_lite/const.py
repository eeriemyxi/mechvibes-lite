import kisesi

from mechvibes_lite import util

log = kisesi.get_logger(__name__)

APP_NAME = "mechvibes-lite"
APP_DESCRIPTION = "Mechvibes Lite is an alternative to Mechvibes (it plays sounds when you press keys."
APP_EPILOG = " * Homepage for Mechvibes Lite is hosted at https://github.com/eeriemyxi/mechvibes-lite "

CONFIG_HOME = util.get_config_path(APP_NAME)
CONFIG_PATH = CONFIG_HOME / "config.ini"
