"""
ABSFUYU
-------
A small collection of code

LINKS
-----
- [Home page](https://pypi.org/project/absfuyu/)
- [Documentation](https://absolutewinter.github.io/absfuyu/)

USAGE
-----

Normal import: 
``import absfuyu``

Using in cmd (`absfuyu[cli]` required): 
``$ fuyu --help``
"""


# Module level
###########################################################################
__title__ = "absfuyu"
__author__ = "AbsoluteWinter"
__license__ = "MIT License"
__all__ = [
    # default
    "util",
    # extra
    "sort", "fun",
    # "pkg_data",
    "game", "tools", "extensions",
    # config
    "config",
    # Other
    "version",
    # "everything",
]


# Library
###########################################################################
from .version import __version__
