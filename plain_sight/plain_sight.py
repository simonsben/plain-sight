from os import environ
from pathlib import Path
from plain_sight.cmd_io import get_input, get_password, get_yes_no
from plain_sight.encryption import decrypt_data, encrypt_data
from plain_sight.file_io import load_file, save_file, json_helper
from json import loads, dumps
from typing import Callable, Dict, Optional, List, Iterable
from plain_sight.log import get_logger
from plain_sight.account import Account
from re import search, Match, compile


logger = get_logger('plain_sight')
_ENCODING = 'utf8'
_MAX_RESULTS = int(environ.get('max_search_results', 10))
_SELECTION_PATTERN = r'(\d+)|(\w?)'
selection_pattern = compile(_SELECTION_PATTERN)
number_pattern = compile(r'\d+')


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
            'n': self.new_account,
            's': self.search_accounts
        }

    @property
    def accounts(self) -> List[Account]:
        """ Accessor for list of accounts """
        accounts = self.plain_data.get('accounts', [])

        if len(accounts) < 1:   # If list is not initialized, attach new list to data
            self.plain_data['accounts'] = accounts

        return accounts

    @staticmethod
    def select_file() -> Path:
        """ Select file to load """
        default_path = Path(environ.get('key_file', 'passwords.vault'))

        while True:
            vault_path = get_input(f'Enter vault path [{default_path}]:', r'.*')

            if vault_path == '':
                print(f'Selected default path: {default_path}')
                return default_path
            elif not Path(vault_path).exists():
                create_new = get_yes_no(f'Create new vault at {vault_path}?')
                if create_new:
                    break

        return Path(vault_path)

    def interaction(self) -> None:
        """ Implements the command line interactivity """
        while True:
            option_choice = get_input('What would you like to do? (h for help)', _SELECTION_PATTERN, 'h')
            logger.debug('Chose %s.', option_choice)

            selection_match = selection_pattern.fullmatch(option_choice)

            if selection_match.group(1):    # If match was a number, it is an account reference
                selection = selection_match.group(0)

                self.view_account(int(selection))
            else:                           # If match was a character, it is a function reference
                option: Callable = self.options.get(option_choice, self.help)

                option()

    def help(self) -> None:
        """ Help function for interactive functionality """
        print('Plain Sight Help\n')
        for option in self.options:
            option_name: str = self.options[option].__name__
            display_name = option_name.replace('_', ' ').capitalize()

            print(f'{option} - {display_name}')

    def list_accounts(self) -> None:
        """ List the accounts in the vault """
        accounts = self.plain_data.get('accounts', [])
        if len(accounts) < 1:
            print('No accounts present in vault.')

        print(self.format_output(accounts))

    def new_account(self) -> None:
        """ Create a new account entry """
        raw_account = Account.collect_info()
        account = Account(raw_account)

        self.accounts.append(account)
        self.updated = True

    def search_accounts(self) -> None:
        """ Search accounts then view or edit """
        while True:
            search_term = get_input('Search term:', default='')
            accounts = [account for account in self.accounts if account.search(search_term)]
            print(self.format_output(accounts)[:_MAX_RESULTS])

            if len(accounts) > _MAX_RESULTS:
                print(f'More than {_MAX_RESULTS} returned, only {_MAX_RESULTS} shown.')

            selection = get_input('Enter index to view account, anything else to exit.', _SELECTION_PATTERN)
            selection_match: Match = search(_SELECTION_PATTERN, selection)

            if selection_match.group(1) is None:
                break

            index = int(selection_match.group(0))
            self.view_account(index, accounts)

    def view_account(self, index: int = None, accounts: List[Account] = None) -> None:
        """ Interact with specific account entity """
        account_pool = accounts if accounts else self.accounts

        if index >= len(account_pool):
            logger.warning(f'Index {index} is larger than the maximum index of {index - 1}.')
        elif index < 0:
            logger.error('Index must be larger than zero.')

        return account_pool[index].interaction(self.set_update_flag)

    def set_update_flag(self) -> None:
        """ Set update flag to True """
        self.updated = True

    @staticmethod
    def load_data(plain_text: str) -> dict:
        """ Load plaintext data into object """
        plain_data: dict = loads(plain_text)
        accounts = plain_data.get('accounts', [])

        plain_data['accounts'] = [Account(account_data) for account_data in accounts]

        return plain_data

    def save_data(self) -> None:
        """ Save data in memory to the same file that was read """
        json_string = dumps(self.plain_data, default=json_helper)
        plain_text = json_string.encode(_ENCODING)
        cipher_text = encrypt_data(self.password, plain_text)

        save_file(self.vault_path, cipher_text)
        logger.debug('Saved file to %s.', self.vault_path)

    def close(self) -> None:
        """ Close application and save data if modified """
        if self.updated:
            will_save = get_yes_no('Would you like to save the changes?')
            if will_save:
                self.save_data()

        del self.password
        del self.plain_data

        exit(0)

    @staticmethod
    def format_output(accounts: Iterable[Account]) -> str:
        output = '\n'.join((f'[{index}] - {account}' for index, account in enumerate(accounts)))

        return output
