"""
Absufyu: Converter
------------------
Convert stuff

Version: 1.1.1
Date updated: 24/11/2023 (dd/mm/yyyy)

Feature:
--------
- Text2Chemistry
- Str2Pixel
"""


# Module level
###########################################################################
__all__ = [
    "Text2Chemistry", "Str2Pixel"
]


# Library
###########################################################################
from itertools import combinations, chain
import math
import re
import string
from typing import List, Union

from absfuyu.core import DATA_PATH, CLITextColor
from absfuyu.logger import logger
from absfuyu.pkg_data import _EXTERNAL_DATA
from absfuyu.util import set_min
from absfuyu.util.api import APIRequest


# Class
###########################################################################
class ChemistryElement:
    """Chemistry Element"""
    def __init__(
            self,
            name: str,
            number: int,
            symbol: str,
            atomic_mass: float
        ) -> None:
        """
        name: element name
        number: order in periodic table
        symbol: short symbol of element
        atomic_mass: atomic mass of element
        """
        self.name = name
        self.number = number
        self.symbol = symbol
        self.atomic_mass = atomic_mass
    def __str__(self) -> str:
        return self.symbol
    def __repr__(self) -> str:
        # return self.symbol
        return f"{self.__class__.__name__}({self.symbol})"

class Text2Chemistry:
    def __init__(self) -> None:
        self.data = APIRequest(
            _EXTERNAL_DATA.get("chemistry.json"),
            encoding="utf-8"
        )
        self.data_location = DATA_PATH.joinpath("chemistry.json")
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    def __repr__(self) -> str:
        return self.__str__()
    
    def _load_chemistry_data(self, update: bool = False) -> List[ChemistryElement]:
        """
        Load chemistry json data from API

        update: Refresh the cache (Default: ``False``)
        """
        json_data = self.data.fetch_data(
            update=update,
            json_cache=self.data_location
        )
        elements = json_data["elements"]
        logger.debug(f"{len(elements)} elements loaded")
        return [
            ChemistryElement(
                name=element["name"],
                number=int(element["number"]),
                symbol=element["symbol"],
                atomic_mass=float(element["atomic_mass"])
            ) for element in elements
        ]
        
    @property
    def unvailable_characters(self):
        """
        Characters that can not be converted (unvailable chemistry symbol)
        
        :rtype: set[str]
        """
        base = set(string.ascii_lowercase)
        available = set("".join(map(lambda x: x.symbol.lower(), self._load_chemistry_data())))
        # logger.debug(base)
        # logger.debug(available)
        return base.difference(available)
    
    def convert(self, text: str) -> List[List[ChemistryElement]]:
        """
        Convert text to chemistry symbol

        :param text: desired text
        :type text: str
        :returns: Converted text (empty list when failed to convert)
        :rtype: list
        """
        # Check if `text` is a word (without digits)
        is_word_pattern = r"^[a-zA-Z]+$"
        if re.search(is_word_pattern, text) is None:
            logger.error("Convert Failed. Word Only!")
            raise ValueError("Convert Failed. Word Only!")
        for x in self.unvailable_characters:
            if text.find(x) != -1:
                logger.debug(f"{text} contains unvailable characters: {self.unvailable_characters}")
                # raise ValueError(f"Text contains {self.unvailable_character}")
                return []
        
        # Setup
        text_lower = text.lower()
        data = self._load_chemistry_data()
        
        # List possible elements
        possible_elements: List[ChemistryElement] = []
        for i, letter in enumerate(text_lower):
            for element in data:
                if element.symbol.lower().startswith(letter): # Check for `element.symbol` starts with `letter`
                    # logger.debug(f"{letter} {element}")
                    if element.symbol.lower().startswith(text_lower[i:i+len(element.symbol)]): # Check for `element.symbol` with len > 1 starts with `letter` of len(element.symbol)
                        possible_elements.append(element)
                    # Break when reach last letter in text
                    if letter == text_lower[-1]:
                        break
        logger.debug(possible_elements)
        if len(possible_elements) < 1: # No possible elements
            return []

        # temp = []
        # for i in range(min_combination_range, len(text_lower)+1):
        #     comb = combinations(possible_elements, i)
        #     temp.append(comb)
        # possible_combinations = chain(*temp)
        max_symbol_len = max(map(lambda x: len(x.symbol), possible_elements)) # Max len of `element.symbol`
        min_combination_range = math.ceil(len(text_lower) / max_symbol_len)
        logger.debug(f"Combination range: [{min_combination_range}, {len(text_lower)}]")
        possible_combinations = chain(*(combinations(possible_elements, i) for i in range(min_combination_range, len(text_lower)+1)))
        # logger.debug(list(possible_combinations))
        
        output = []
        for comb in possible_combinations:
            merged = "".join(map(lambda x: x.symbol, comb))
            if text_lower == merged.lower():
                output.append(list(comb))
                logger.debug(f"Found: {merged}")

        return output


class Str2Pixel:
    """Convert str into pixel"""
    PIXEL = u"\u2588"
    def __init__(
            self,
            str_data: str,
            *,
            pixel_size: int = 2,
            pixel_symbol_overwrite: Union[str, None] = None
        ) -> None:
        """
        str_data: Pixel string data (Format: <number_of_pixel><color_code>)
        pixel_size: Pixel size (Default: 2)
        pixel_symbol_overwrite: Overwrite pixel symbol (Default: None)

        Example: 50w20b = 50 white pixels and 20 black pixels
        """
        self.data = str_data
        if pixel_symbol_overwrite is None:
            self.pixel = self.PIXEL * set_min(pixel_size, min_value=1)
        else:
            self.pixel = pixel_symbol_overwrite
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(pixel={self.pixel})"
    def __repr__(self) -> str:
        return self.__str__()
    
    def _extract_pixel(self):
        """Split str_data into corresponding int and str"""
        num = re.split("[a-zA-Z]", self.data)
        num = filter(lambda x: x != "", num) # Clean "" in list
        num = list(map(int, num))
        char = re.split("[0-9]", self.data)
        char = filter(lambda x: x != "", char)
        return [x for y in zip(num, char) for x in y]

    def convert(self, line_break: bool = True) -> str:
        """
        Convert data into pixel
        
        :param line_break: add ``\\n`` at the end of line (Default: ``False``)
        :type line_break: bool
        :returns: Converted colored pixels
        :rtype: str
        """
        # Extract pixel
        pixel_map = self._extract_pixel()

        # Translation to color
        translate = {
            "w": CLITextColor.WHITE,
            "b": CLITextColor.BLACK, 
            "B": CLITextColor.BLUE, 
            "g": CLITextColor.GRAY, 
            "G": CLITextColor.GREEN, 
            "r": CLITextColor.RED, 
            "R": CLITextColor.DARK_RED, 
            "m": CLITextColor.MAGENTA, 
            "y": CLITextColor.YELLOW, 
            "E": CLITextColor.RESET,
            "N": "\n" # New line
        }

        # import colorama
        # translate = {
        #     "w": colorama.Fore.WHITE,
        #     "b": colorama.Fore.BLACK,
        #     "B": colorama.Fore.BLUE,
        #     "g": colorama.Fore.LIGHTBLACK_EX, # Gray
        #     "G": colorama.Fore.GREEN,
        #     "r": colorama.Fore.LIGHTRED_EX,
        #     "R": colorama.Fore.RED, # Dark red
        #     "m": colorama.Fore.MAGENTA,
        #     "y": colorama.Fore.YELLOW,
        #     "E": colorama.Fore.RESET,
        #     "N": "\n", # New line
        # }

        # Output
        out = ""
        for i, x in enumerate(pixel_map):
            if isinstance(x, str):
                temp = self.pixel * pixel_map[i-1]
                out += f"{translate[x]}{temp}{translate['E']}"
        if line_break:
            return out + "\n"
        else:
            return out


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)