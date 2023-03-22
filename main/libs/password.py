import os
from hashlib import pbkdf2_hmac

from main.commons import const


def generate_salt() -> str:
    return os.urandom(const.SALT_BYTE_LEN).hex()


def hash_password(password: str, salt: str):
    # check salt must be hex string
    try:
        salt_byte = bytes.fromhex(salt)
    except ValueError:
        raise ValueError("'salt' must be hex string")

    return pbkdf2_hmac(
        const.HASH_ALGO, password.encode(), salt_byte, const.HASH_ITERS
    ).hex()


def verify_password(password: str, hashed_password: str, salt: str):
    return hash_password(password, salt) == hashed_password
