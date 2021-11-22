from plain_sight.account import Account
from plain_sight.encryption import get_character_range


_SYSIN = 'builtins.input'


def test_load() -> None:
    start = 'a'
    end = 'b'
    data_to_load = {character: index for index, character in enumerate(get_character_range(start, end))}

    _account = Account(data_to_load)

    for key in data_to_load:
        assert getattr(_account, key) == data_to_load.get(key)


def test_collection(mocker) -> None:
    account_info = {
        'name': 'my name',
        'login': 'my login',
        'password': 'mypassword'
    }

    inputs = list(account_info.values())
    inputs.insert(2, 'n')

    mocker.patch(_SYSIN, side_effect=inputs)
    account = Account.collect_info()

    assert len(account) == len(account_info)
    for key in account_info:
        assert key in account
        assert account_info[key] == account.get(key, '')


def test_new_password(mocker) -> None:
    valid_password = ['n', 'val1dp@s5word']
    mocker.patch(_SYSIN, side_effect=valid_password)

    valid_collection = Account.new_password()
    assert valid_password[-1] == valid_collection


def test_invalid_password(mocker) -> None:
    invalid_password = ['n', 'invalid password']
    mocker.patch(_SYSIN, side_effect=invalid_password)

    invalid_collection = Account.new_password()
    assert invalid_password[-1] != invalid_collection
    assert invalid_collection is None


def test_generate_password(mocker) -> None:
    default_length = ['y', '']
    custom_length = ['y', '12']

    mocker.patch(_SYSIN, side_effect=default_length)
    default_generation = Account.new_password()

    assert len(default_generation) == 20

    mocker.patch(_SYSIN, side_effect=custom_length)
    custom_generation = Account.new_password()

    assert len(custom_generation) == int(custom_length[-1])
