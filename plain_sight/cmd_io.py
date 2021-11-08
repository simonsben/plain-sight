from re import fullmatch
from typing import Union


def get_input(prompt: str, validation: str = '.+', default: Union[str, None] = None) -> Union[str, None]:
    response = input(prompt)

    if fullmatch(validation, response) is None:
        return default
    return response


def get_password():
    return get_input('Password: ', r'[!@#$%^&*\w\d]+')


def get_yes_no(message: str) -> bool:
    """ Get answer to yes/no response """
    response = ''
    while not response or len(response) < 1:
        response = get_input(f'{message} (y/n) ', r'[yn]')

    return response == 'y'

