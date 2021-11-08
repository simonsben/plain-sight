from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from hashlib import sha256
from secrets import SystemRandom, token_bytes


_ALGORITHM = algorithms.AES
_PAD_ALGORITHM = PKCS7
_MODE = modes.CBC
_IV_LENGTH = 16
_PASSWORD_LENGTH = 20
_ENCODING = 'utf8'


def encrypt_data(key: str, data: bytes) -> bytes:
    """ Compute ciphertext from plaintext """
    byte_key = sha256(key.encode(_ENCODING)).digest()
    iv = token_bytes(_IV_LENGTH)

    cipher = Cipher(_ALGORITHM(byte_key), _MODE(iv))
    encryptor = cipher.encryptor()

    padder = _PAD_ALGORITHM(_ALGORITHM.block_size).padder()
    data = padder.update(data) + padder.finalize()

    cipher_text = iv + encryptor.update(data) + encryptor.finalize()
    return cipher_text


def get_character_range(start: str, end: str) -> list:
    """ Return a list of characters """
    start_index = ord(start)
    end_index = ord(end) + 1

    return [chr(char_index) for char_index in range(start_index, end_index)]


def decrypt_data(key: str, cipher_data: bytes) -> bytes:
    """ Compute plaintext from ciphertext """
    byte_key = sha256(key.encode(_ENCODING)).digest()

    if len(cipher_data) < _IV_LENGTH:
        return b'{}'

    iv, cipher_text = cipher_data[:_IV_LENGTH], cipher_data[_IV_LENGTH:]

    cipher = Cipher(_ALGORITHM(byte_key), _MODE(iv))
    decrypter = cipher.decryptor()

    plain_text = decrypter.update(cipher_text) + decrypter.finalize()

    unpadder = _PAD_ALGORITHM(_ALGORITHM.block_size).unpadder()

    try:
        plain_text = unpadder.update(plain_text) + unpadder.finalize()
    except ValueError:
        print('Invalid password entered. Exiting.')
        exit(0)

    return plain_text


def generate_password(length: int = _PASSWORD_LENGTH) -> str:
    """ Securely generate password """
    lower = get_character_range('a', 'z')
    upper = get_character_range('A', 'Z')
    digits = get_character_range('0', '9')
    special = ['!', '@', '#', '$', '%', '^', '&', '*']

    population = lower + upper + digits + special
    generator = SystemRandom()

    password = generator.choices(population, k=length)
    return ''.join(password)
