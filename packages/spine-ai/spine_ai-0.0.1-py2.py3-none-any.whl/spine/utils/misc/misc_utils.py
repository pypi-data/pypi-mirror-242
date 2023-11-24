"""
Misc utils, mainly for sanity checks and functions to be used within cli.py

Written by: Aaron Ward
"""

import logging
from datetime import date
from pathlib import Path

logger = logging.getLogger('spine.utils.misc')

def read_txt_file(path):
    """
    Reads a text file and returns its content as a string.

    Args:
        path (str): The path to the text file.

    Returns:
        str: The content of the text file as a string.

    Raises:
        FileNotFoundError: If the file specified by the path does not exist.
        IOError: If there was an error reading the file.

    Example:
        >>> content = read_txt_file('path/to/file.txt')
        >>> print(content)
        This is the content of the text file.
    """
    try:
        with open(path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{path}' does not exist.")
    except IOError:
        raise IOError(f"Error reading file '{path}'.")



def check_existence(file_path):
    """
    Function for checking if config file path exists

    args:
        file_path: path of a file or directory
    """

    if not Path(file_path).expanduser().exists():
        logger.error(
            f"Exception: File or directory doesn't exist in: {file_path}\n"
            "Please re-check your config values and try again.")

    return True

def check_config_file(config):
    """
    This function works as a sanity check on the values withing the config
    file. If the required parameters have not been filled out the CLI tool will
    exit and an exception is thrown.

    args:
        config (dict): from config yaml file
    """

    for key in config.keys():
        # If the key is not of dict datatype
        if not isinstance(config[key], dict):
            if config[key] == "":
                logger.error(
                    f"{key} is an empty string. Make sure to populate the config file.")

            # Check path parameters
            # if key == "paths":
            #     if not config['paths']['file'] or not config['paths']['file']:
            #         logger.error(
            #             "You must specify a <some file>")


            # Check document files
            # if key == "reference_files":
            #     for file in config['reference_files'].keys():
            #         if not config['reference_files'][file][-1]:
            #             logger.error(
            #                 "You must specify the suitable reference files")
            #         else:
            #             check_existence(
            #                 Path(
            #                     *config['reference_files'][file]).expanduser())



    logger.info("Config file is valid")