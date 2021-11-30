from pathlib import Path
from typing import Union
from plain_sight.log import get_logger
from json import loads
from os import environ


CONFIG_FILENAME = 'config.json'
CONFIG_TEMPLATE_FILENAME = 'config.template.json'


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


# TODO figure out how to use logger instead of prints (import order)
def load_config(filename: Union[Path, str] = CONFIG_FILENAME) -> dict:
    """ Load config and parse to dict """
    if isinstance(filename, str):
        filename = Path(filename)

    file_name = filename.name
    full_path = filename.absolute().parent
    for _ in range(3):
        if (full_path / file_name).exists():
            break
        full_path = full_path.parent

    filename = full_path / file_name
    if not (full_path / file_name).exists():
        raise FileNotFoundError(f'Config file, {filename}, could not be found.')

    data = load_file(filename)
    config = {}

    try:
        config = data.decode('utf8')
        config = loads(config)
    except Exception:
        print(f'Error decoding config data from {filename}.')

    # Make config environment variables
    for key in config:
        environ[key] = str(config[key])

    return config


def json_helper(obj):
    """ Specifies the name of the helper function for exporting to json """
    return obj.to_json()


_filename = CONFIG_FILENAME if Path(CONFIG_FILENAME).exists() else CONFIG_TEMPLATE_FILENAME
load_config(_filename)

logger = get_logger('file_io')
logger.info('Config loaded from %s.', _filename)
