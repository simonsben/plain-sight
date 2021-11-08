from pathlib import Path
from typing import Union
from plain_sight.log import get_logger
from json import loads
from os import environ


def load_file(filename: Union[Path, str]) -> bytes:
    """ Load file as bytes """
    if isinstance(filename, str):
        filename = Path(filename)

    try:
        with filename.open('rb') as fl:
            data = fl.read()

    except Exception as e:
        logger.error('Error opening %s.', str(filename), exc_info=e)
        return b''

    return data


def save_file(filename: Union[Path, str], data: bytes) -> None:
    """ Save file to bytes """
    if isinstance(filename, str):
        filename = Path(filename)

    try:
        with filename.open('wb') as fl:
            fl.write(data)
    except Exception as e:
        logger.error('Error writing to %s.', str(filename), exc_info=e)


def load_config(filename: Union[Path, str] = 'config.json') -> dict:
    """ Load config and parse to dict """
    data = load_file(filename)
    config = {}

    try:
        config = data.decode('utf8')
        config = loads(config)
    except Exception as e:
        logger.error('Error decoding config data from %s.', str(filename), exc_info=e)

    # Make config environment variables
    for key in config:
        environ[key] = config[key]

    return config


load_config()
logger = get_logger('file_io')
