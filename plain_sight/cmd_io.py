from re import fullmatch
from typing import Union


def get_input(prompt: str, validation: str = '.+', default: Union[str, None] = None) -> Union[str, None]:
    """ Get input from command line """
    response = input(prompt + ' ')

    if type(response) not in {str, bytes}:
        return default

    if fullmatch(validation, response) is None:
        return default
    return response


def get_password() -> str:
    """ Collect password input """
    return get_input('Password: ', r'[!@#$%^&*\w\d]+')


def get_yes_no(message: str) -> bool:
    """ Get answer to yes/no response """
    response = ''
    while not response or len(response) < 1:
        response = get_input(f'{message} (y/n) ', r'[yn]')

    return response == 'y'
