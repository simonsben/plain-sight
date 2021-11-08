from os import environ
from pathlib import Path
from plain_sight.cmd_io import get_input, get_password, get_yes_no
from plain_sight.encryption import decrypt_data, encrypt_data
from plain_sight.file_io import load_file, save_file
from json import loads, dumps
from typing import Callable, Dict, Optional, List
from plain_sight.log import get_logger
from plain_sight.account import Account


logger = get_logger('plain_sight')
_ENCODING = 'utf8'


class PlainSight:
    def __init__(self):
        self.updated: bool = False

        self.vault_path: Path = self.select_file()
        self.password: str = get_password()

        if self.vault_path.exists():
            cipher_text: bytes = load_file(self.vault_path)
            plain_text: str = decrypt_data(self.password, cipher_text).decode(_ENCODING)
        else:
            create_new = get_yes_no(f'Would you like to make a new vault at {str(self.vault_path)}?')
            if not create_new:
                exit(0)
            plain_text = '{}'

        self.plain_data: dict = self.load_data(plain_text)

        self.options: Dict[str, Callable[[Optional[int]], None]] = {
            'l': self.list_accounts,
            'c': self.close,
            'h': self.help,
            'n': self.new_account
        }

    @property
    def accounts(self) -> List[Account]:
        accounts = self.plain_data.get('accounts', [])

        if len(accounts) < 1:
            self.plain_data['accounts'] = accounts

        return accounts

    @staticmethod
    def select_file() -> Path:
        default_path = Path(environ.get('key_file', 'passwords.vault'))

        while True:
            vault_path = get_input(f'Enter vault path [{default_path}]: ', r'.*')

            if vault_path == '':
                print(f'Selected default path: {default_path}')
                return default_path
            elif not Path(vault_path).exists():
                create_new = get_yes_no(f'Create new vault at {vault_path}?')
                if create_new:
                    break

        return Path(vault_path)

    def interaction(self) -> None:
        while True:
            option_choice = get_input('What would you like to do? (h for help) ', r'\w{1}', 'h')
            logger.debug('Chose %s.', option_choice)

            option: Callable = self.options.get(option_choice, self.help)

            option()

    def help(self) -> None:
        print('Plain Sight Help\n')
        for option in self.options:
            option_name: str = self.options[option].__name__
            display_name = option_name.replace('_', ' ').capitalize()

            print(f'{option} - {display_name}')

    def list_accounts(self) -> None:
        accounts = self.plain_data.get('accounts', [])
        if len(accounts) < 1:
            print('No accounts present in vault.')

        for index, account in enumerate(accounts):
            print(f'[{index}] - {account}')

    def new_account(self) -> None:
        account = Account()
        account.create()

        self.accounts.append(account)
        self.updated = True

    @staticmethod
    def load_data(plain_text: str) -> dict:
        plain_data: dict = loads(plain_text)
        accounts = plain_data.get('accounts', [])

        plain_data['accounts'] = [Account(account_data) for account_data in accounts]

        return plain_data

    def save_data(self) -> None:
        json_string = dumps(self.plain_data, default=lambda obj: getattr(obj, 'json_helper')())
        plain_text = json_string.encode(_ENCODING)
        cipher_text = encrypt_data(self.password, plain_text)

        save_file(self.vault_path, cipher_text)

    def close(self) -> None:
        if self.updated:
            will_save = get_yes_no('Would you like to save the changes?')
            if will_save:
                self.save_data()

        del self.password
        del self.plain_data

        exit(0)
