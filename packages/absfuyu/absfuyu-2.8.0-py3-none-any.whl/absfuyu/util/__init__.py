"""
Absufyu: Utilities
---
Some random utilities

Version: 1.4.3
Date updated: 22/11/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pkgutil
# import sys
from typing import Union

from absfuyu.logger import logger


# Function
###########################################################################
def get_installed_package():
    """
    Return a list of installed packages
    """
    iter_modules = list({module.name for module in pkgutil.iter_modules() if module.ispkg})
    # builtin = sys.builtin_module_names
    # return set.union(iter_modules, builtin)
    return sorted(iter_modules)


def set_min(
        current_value: Union[int, float],
        *,
        min_value: Union[int, float] = 0,
    ) -> Union[int, float]:
    """
    Return `min value` when `current_value` < `min_value`
    """
    if current_value < min_value:
        current_value = min_value
    return current_value

def set_max(
        current_value: Union[int, float],
        *,
        max_value: Union[int, float] = 100,
    ) -> Union[int, float]:
    """
    Return `max value` when `current_value` > `max_value`
    """
    if current_value > max_value:
        current_value = max_value
    return current_value

def set_min_max(
        current_value: Union[int, float],
        *,
        min_value: Union[int, float] = 0,
        max_value: Union[int, float] = 100
    ) -> Union[int, float]:
    """
    Return `min or max value` when `current_value` is outside `[min_value, max_value]`
    """
    current_value = set_min(current_value, min_value=min_value)
    current_value = set_max(current_value, max_value=max_value)
    return current_value


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)