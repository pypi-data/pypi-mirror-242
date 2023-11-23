"""
Absufyu: Utilities
---
Some random utilities

Version: 1.4.2
Date updated: 18/11/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pkg_resources
from typing import Union

from absfuyu.logger import logger


# Function
###########################################################################
def get_installed_package(version_included: bool = False):
    """
    Return a list of installed packages
    """
    installed_packages = pkg_resources.working_set
    if version_included:
        installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
            for i in installed_packages])
        logger.debug(installed_packages_list)
        return installed_packages_list
    else:
        out = sorted([x.key for x in installed_packages])
        logger.debug(out)
        return out


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