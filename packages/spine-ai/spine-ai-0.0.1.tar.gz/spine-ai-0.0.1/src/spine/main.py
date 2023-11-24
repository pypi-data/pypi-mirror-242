"""
This is the main driver program for spine. 

Written by: Aaron Ward
"""
import os
import json
import logging
import configparser
from pathlib import Path

from spine.utils.misc import (logging_utils, misc_utils)
from spine.utils.env_utils import get_openai_key

logger = logging.getLogger(__name__)
logging_utils.log_to_console(__name__, is_header=True)

def run(config):
    """
    This is the main run function of the spine application. 
    It spins up the spine server, appropraite nodes and 
    the chat interface.

    Args:
        - config (configparser): config passed to spine run
    Returns:
        - None
    """

if __name__ == "__main__":
    pass
