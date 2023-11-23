"""
Test: Everything

Version: 1.1.0
Date updated: 18/11/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu import everything as ab

# --- Loading test --------------------------------------------------------
EVERYTHING = False
try:
    # from absfuyu.core import *
    from absfuyu.core import (
        ModulePackage, ModuleList,
        Color, CLITextColor,
        CORE_PATH, CONFIG_PATH, DATA_PATH
    )
    # from absfuyu.logger import *
    from absfuyu.logger import logger, LogLevel
    from absfuyu.sort import (
        selection_sort, insertion_sort,
        alphabetAppear,
        linear_search, binary_search
    )
    from absfuyu.version import Version, check_for_update

    # --- Sub-package ---
    from absfuyu.collections import Dummy, ClassBase
    from absfuyu.collections.content import ContentLoader, Content, LoadedContent # Has unidecode
    from absfuyu.collections.data_extension import Text, IntNumber, ListKai, DictKai
    from absfuyu.collections.generator import Charset, Generator
    from absfuyu.collections.human import BloodType, Human, Person # Has python-dateutil

    from absfuyu.config import *

    from absfuyu.extensions import *
    from absfuyu.extensions.beautiful import beautiful_output, demo # Has rich
    from absfuyu.extensions.extra import *
    from absfuyu.extensions.extra.data_analysis import ( # Has pandas, numpy
        summary, divide_dataframe, delta_date, modify_date,
        equalize_df, compare_2_list, rename_with_dict, threshold_filter,
        PLTFormatString,
        _DictToAtrr,
        MatplotlibFormatString,
        DataFrameKai
    )

    from absfuyu.fun import zodiac_sign, im_bored, force_shutdown, happy_new_year
    from absfuyu.fun.tarot import Tarot, TarotCard
    from absfuyu.fun.WGS import WGS, Str2Pixel

    from absfuyu.game import game_escapeLoop, game_RockPaperScissors
    from absfuyu.game.sudoku import Sudoku
    from absfuyu.game.tictactoe import *
    from absfuyu.game.wordle import Wordle # Has requests

    from absfuyu.pkg_data import PkgData, PACKAGE_DATA

    from absfuyu.tools import *
    from absfuyu.tools.converter import ChemistryElement, Text2Chemistry
    from absfuyu.tools.keygen import Keygen
    from absfuyu.tools.obfuscator import Obfuscator, ObfuscatorLibraryList
    from absfuyu.tools.stats import ListStats
    from absfuyu.tools.web import soup_link, gen_random_commit_msg # Has bs4, requests

    from absfuyu.util import get_installed_package, set_max, set_min, set_min_max
    from absfuyu.util.api import APIRequest, ping_windows # Has requests
    from absfuyu.util.json_method import JsonFile, load_json
    from absfuyu.util.lunar import LunarCalendar
    from absfuyu.util.path import Directory, SaveFileAs
    from absfuyu.util.performance import measure_performance, source_this, var_check
    from absfuyu.util.pkl import Pickler
    from absfuyu.util.zipped import Zipper

    from absfuyu.contrib import *
    from absfuyu.unused import *

    EVERYTHING = True

except:
    EVERYTHING = False


# Test
###########################################################################
# def test_ev():
#     assert ab.__IS_EVERYTHING is True

def test_everything():
    assert EVERYTHING is True