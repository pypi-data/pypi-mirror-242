"""
Entry point script for the fleet CLI tool.
Terminal commands and options are specified here.

Written by: Aaron Ward
"""
import ast
import yaml
import click
import logging
import configparser
from pathlib import Path
from pyfiglet import Figlet
from termcolor import colored

from spine import main
from spine.utils.misc import logging_utils
from spine.utils.misc.misc_utils import *

logger = logging.getLogger(__name__)
logging_utils.log_to_console(__name__, is_header=True)
logging_utils.log_to_console('spine.utils.misc')

# for FONTS in `pyfiglet -l`; do echo $FONTS; pyfiglet $FONTS -f $FONTS; done;
print(colored(Figlet(font="univers").renderText("Spine"), "magenta"))


############### CLI Commands ###############
@click.group()
def cli():
    """
    \033[0;35m
    * Spine: Autonomous Agent Orchestration
     \033[0;0m
    """
    pass


@cli.command()
@click.option('--config-path',
              help='Path to config file containing parameters and modelling templates, copy from config_template.yml',
              required=True)
def run(config_path):
    """
    Run the spine server

    \033[0;35mexample: spine run --config-path="./config.yml"\033[0;0m
    """
    logger.info("Running spine run command")
    check_existence(config_path)
    config = configparser.RawConfigParser()
    config.read(config_path)
        
    # TODO: Update with config validation rather than yaml/dict
    # https://docs.python.org/3/library/configparser.html#
    config_dict = dict(config.items())
    check_config_file(config_dict)

    # run the pipeline
    main.run(config)
    