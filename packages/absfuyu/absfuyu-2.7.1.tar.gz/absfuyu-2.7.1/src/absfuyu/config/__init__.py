"""
ABSFUYU
-------
Configuration
"""



# Library
##############################################################
import json as __json
import os as __os
from typing import Optional as __Optional
from typing import Any as __Any

from absfuyu.config.config2 import ABSFUYU_CONFIG, Config


# Define
##############################################################
__here = __os.path.abspath(__os.path.dirname(__file__))
CONFIG_LOC = __os.path.join(__here, "config.json")
__config_name = "config"



# Function
##############################################################
def __load_cfg(config_name: str = __config_name):
    """Load configuration file"""
    with open(f"{__here}/{config_name}.json") as json_cfg:
        cfg = __json.load(json_cfg)
    return cfg

def __save_cfg(config, config_name: str = __config_name):
    """Save config"""
    cfg = __json.dumps(config, indent=4, sort_keys=True)
    with open(f"{__here}/{config_name}.json","w") as json_cfg:
        json_cfg.writelines(cfg)
    return None

def change_cfg(setting: str, value: __Any):
    """Change setting in config"""
    cfg: dict = __load_cfg()
    if setting in cfg["setting"]:
        cfg["setting"][setting]["value"] = value
        __save_cfg(cfg)
    else:
        raise SystemExit("Setting unvailable")
    
    global CONFIG
    CONFIG = __load_cfg()

def reset_cfg():
    """Reset config to default value"""
    # Rewrite this
    cfg: dict = __load_cfg()
    for setting in cfg["setting"]:
        cfg["setting"][setting]["value"] = cfg["setting"][setting]["default"]
    __save_cfg(cfg)
    global CONFIG
    CONFIG = __load_cfg()
    pass

def show_cfg(
        setting: __Optional[str] = None,
        raw: bool = False
    ):
    """
    Show value of setting
    
    If raw = True then return the raw value
    """
    cfg: dict = __load_cfg()
    if setting is None:
        if raw:
            return cfg["setting"]
        else:
            return dict(zip(
                [x for x in cfg["setting"].keys()],
                [x["value"] for x in cfg["setting"].values()]
            ))

    else:
        if setting in cfg["setting"]:
            if raw:
                return cfg["setting"][setting]["value"]
            else:
                return f"{setting} = {cfg['setting'][setting]['value']}"
        else:
            raise SystemExit("Setting unvailable")

def toggle_setting(setting: str):
    """
    Toggle on/off for each setting
    
    If setting type is bool
    """
    cfg: dict = __load_cfg()
    if setting in cfg["setting"]:
        setting_state = cfg["setting"][setting]["value"]
        if isinstance(setting_state, bool):
            if setting_state:
                change_cfg(setting, False)
            else:
                change_cfg(setting, True)
        else:
            raise SystemExit("This setting is not type: bool")
    pass


def welcome():
    cfg: dict = __load_cfg()
    if cfg["setting"]["first-run"]["value"]:
        change_cfg("first-run", False)
        # Do other stuff here
    pass


# Config
##############################################################
CONFIG = __load_cfg()