"""
Absfuyu: Core
---
Contain type hints and other stuffs

Version: 2.1.4
Date updated: 23/11/2023 (dd/mm/yyyy)
"""


# Module Package
###########################################################################
ModulePackage = [
    "all",
    "cli",
    "beautiful", "extra",
    "full",
    "dev"
]
ModuleList = [
    "collections",
    "config",
    "extensions",
    "fun",
    "game",
    "pkg_data",
    "sort",
    "tools",
    "util",
    "version",
]


# Library
###########################################################################
from pathlib import Path

try:
    import colorama as __colorama
except ImportError:
    __colorama = None


# Color - colorama
###########################################################################
if __colorama is not None:
    # __colorama.init(autoreset=True)
    Color = {
        "green": __colorama.Fore.LIGHTGREEN_EX,
        "GREEN": __colorama.Fore.GREEN,
        "blue": __colorama.Fore.LIGHTCYAN_EX,
        "BLUE": __colorama.Fore.CYAN,
        "red": __colorama.Fore.LIGHTRED_EX,
        "RED": __colorama.Fore.RED,
        "yellow": __colorama.Fore.LIGHTYELLOW_EX,
        "YELLOW": __colorama.Fore.YELLOW,
        "reset": __colorama.Fore.RESET
    }
else:
    Color = {
        "green": "",
        "GREEN": "",
        "blue": "",
        "BLUE":"",
        "red": "",
        "RED": "",
        "yellow": "",
        "YELLOW": "",
        "reset": ""
    }


class CLITextColor:
    """Color code for text in terminal"""
    WHITE     = "\x1b[37m"
    BLACK     = "\x1b[30m"
    BLUE      = "\x1b[34m"
    GRAY      = "\x1b[90m"
    GREEN     = "\x1b[32m"
    RED       = "\x1b[91m"
    DARK_RED  = "\x1b[31m"
    MAGENTA   = "\x1b[35m"
    YELLOW    = "\x1b[33m"
    RESET     = "\x1b[39m"


# Path
###########################################################################
# CORE_PATH = Path(os.path.abspath(os.path.dirname(__file__)))
CORE_PATH = Path(__file__).parent.absolute()
CONFIG_PATH = CORE_PATH.joinpath("config", "config.json")
DATA_PATH = CORE_PATH.joinpath("pkg_data")

