import plain_sight.encryption as encryption
from typing import Callable, Hashable
from functools import partial


_PLAINTEXT = 'Hello, world!'
_KEY = 'this is my key'


def ensure_unique(generator: Callable[[], Hashable],  num_copies: int = 1000) -> None:
    copies = set((generator() for _ in range(num_copies)))

    assert len(copies) == num_copies


def test_character_range() -> None:
    start = 'A'
    end = 'Z'

    character_range = encryption.get_character_range(start, end)
    assert len(character_range) == 26

    assert character_range[0] == 'A'
    assert character_range[-1] == 'Z'

    for index, character in enumerate(character_range[:-1]):
        assert chr(ord(start) + index) == character


def test_unique_encryption():
    plaintext_bytes = _PLAINTEXT.encode()
    generator = partial(encryption.encrypt_data, key=_KEY, data=plaintext_bytes)

    ensure_unique(generator)


def test_encryption():
    ciphertext = encryption.encrypt_data(_KEY, _PLAINTEXT.encode())
    recovered_plaintext = encryption.decrypt_data(_KEY, ciphertext)

    assert _PLAINTEXT == recovered_plaintext.decode()
    assert ciphertext != _PLAINTEXT
    assert ciphertext != recovered_plaintext


def test_unique_password() -> None:
    ensure_unique(encryption.generate_password, num_copies=10000)
