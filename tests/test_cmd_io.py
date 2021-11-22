import plain_sight.cmd_io as cmd


_SYSIN = 'builtins.input'
_PROMPT = 'example prompt'
_VALID_INPUT = 'some valid input'
_INVALID_INPUT = ''

_VALID_PASSWORD = 'someval1dp@s5worD'
_INVALID_PASSWORD = 'someval1dp@s5wor>'


def test_input(mocker) -> None:
    mocker.patch(_SYSIN, side_effect=[_VALID_INPUT])

    collected_input = cmd.get_input(_PROMPT)
    assert _VALID_INPUT == collected_input


def test_invalid_input(mocker) -> None:
    mocker.patch(_SYSIN, side_effect=[_INVALID_INPUT])

    collected_input = cmd.get_input(_PROMPT)
    assert _INVALID_INPUT != collected_input
    assert collected_input is None


def test_default_value(mocker) -> None:
    mocker.patch(_SYSIN, side_effect=[_INVALID_INPUT])

    collected_input = cmd.get_input(_PROMPT, default=_VALID_INPUT)
    assert collected_input == _VALID_INPUT
    assert collected_input != _INVALID_INPUT


def test_get_password(mocker) -> None:
    mocker.patch(_SYSIN, side_effect=[_VALID_PASSWORD])

    collected_password = cmd.get_password()
    assert _VALID_PASSWORD == collected_password


def test_invalid_get_password(mocker) -> None:
    mocker.patch(_SYSIN, side_effect=[_INVALID_PASSWORD])

    collected_password = cmd.get_password()
    assert _INVALID_PASSWORD != collected_password
    assert collected_password is None


def test_yes_no(mocker) -> None:
    yes_input = ['y']
    no_input = ['n']
    retry_input = ['1', '7', 'c', 'Q', '!', 'y']

    mocker.patch(_SYSIN, side_effect=yes_input)
    collected_yes = cmd.get_yes_no(_PROMPT)
    assert collected_yes is True

    mocker.patch(_SYSIN, side_effect=no_input)
    collected_no = cmd.get_yes_no(_PROMPT)
    assert collected_no is False

    mocker.patch(_SYSIN, side_effect=retry_input)
    collected_retry = cmd.get_yes_no(_PROMPT)
    assert collected_retry is True
