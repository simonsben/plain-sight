from plain_sight.cmd_io import get_input, get_password, get_yes_no
from plain_sight.encryption import generate_password, _PASSWORD_LENGTH


class Account:
    def __init__(self, package: dict = None):
        self.name: str = ''
        self.login: str = ''
        self.password: str = ''

        if package is not None:
            self.load(package)

    def load(self, data: dict) -> None:
        for key in data:
            setattr(self, key, data[key])

    def create(self):
        self.name = get_input('Enter name of new account: ')
        self.login = get_input('Enter login name: ')

        will_generate_password = get_yes_no('Would you like generate a password?')
        if will_generate_password:
            password_length = int(get_input(f'Enter password length [{_PASSWORD_LENGTH}]: ', r'\d+', '20'))
            self.password = generate_password(password_length)
        else:
            self.password = get_password()

    def json_helper(self):
        return {
            'name': self.name,
            'login': self.login,
            'password': self.password
        }

    def __str__(self) -> str:
        return self.name
