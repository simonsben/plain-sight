from plain_sight.cmd_io import get_input, get_password, get_yes_no
from plain_sight.encryption import generate_password, _PASSWORD_LENGTH
from typing import Dict, Callable, Optional, List, Union
from plain_sight.log import get_logger
from re import compile


_SKIP_ATTRIBUTES = {'options', 'password'}
logger = get_logger('account')
builtin_pattern = compile(r'(__\w+__)|(options)')


class Account:
    def __init__(self, package: dict = None):
        if package is not None:
            self.load(package)

        self.options: Dict[str, Callable[[Optional[int]], None]] = {
            'c': self.close,
            'v': self.view_account,
            'p': self.get_password,
            # 'e': self.edit,
            'h': self.help
        }

    def load(self, data: dict) -> None:
        """ Load data from dictionary """
        for key in data:
            setattr(self, key, data[key])

    def close(self) -> None:
        """ No action required """
        pass

    @staticmethod
    def collect_info() -> dict:
        """ Create new account """
        package = {
            'name': get_input('Enter name of new account: '),
            'login': get_input('Enter login name: ')
        }

        will_generate_password = get_yes_no('Would you like generate a password?')
        if will_generate_password:
            password_length = int(get_input(f'Enter password length [{_PASSWORD_LENGTH}]: ', r'\d+', '20'))
            package['password'] = generate_password(password_length)
        else:
            package['password'] = get_password()

        return package

    def interaction(self) -> None:
        """ Implements the command line interactivity """
        while True:
            option_choice = get_input('Account operation? (h for help) ', r'\w{1}', 'h')
            logger.debug('Chose %s.', option_choice)

            if option_choice == 'c':
                break

            option: Callable = self.options.get(option_choice, self.help)

            option()

    def help(self) -> None:

        print('Plain Sight Account Help\n')
        for option in self.options:
            option_name: str = self.options[option].__name__
            display_name = option_name.replace('_', ' ').capitalize()

            print(f'{option} - {display_name}')

    def to_json(self) -> Dict[str, Union[str, int]]:
        """ Used to help export object to json """
        attributes = self.get_attributes()

        return {attribute: getattr(self, attribute) for attribute in attributes}

    def __str__(self) -> str:
        return getattr(self, 'name')

    def get_attributes(self) -> List:
        attributes = []

        for attribute in dir(self):
            actual = getattr(self, attribute)

            is_builtin = builtin_pattern.match(attribute) is not None
            is_callable = callable(actual)
            if is_builtin or is_callable:
                continue

            attributes.append(attribute)

        return attributes

    def get_password(self) -> None:
        password = getattr(self, 'password')
        print('Password: ', password)

    def view_account(self) -> None:
        for attribute in self.get_attributes():
            if attribute in _SKIP_ATTRIBUTES:
                continue
            print(f'{attribute}: {getattr(self, attribute)}')

    def search(self, search_term) -> bool:
        name = getattr(self, 'name')
        login = getattr(self, 'login')

        return search_term in name or login
