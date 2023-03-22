import os
from hashlib import pbkdf2_hmac

from main.commons import const


def generate_salt() -> str:
    return os.urandom(const.SALT_BYTE_LEN).hex()


def hash_password(password: str, salt: str) -> str:
    # check salt must be hex string
    return pbkdf2_hmac(
        const.HASH_ALGO, password.encode(), bytes.fromhex(salt), const.HASH_ITERS
    ).hex()


def verify_password(password: str, hashed_password: str, salt: str):
    return hash_password(password, salt) == hashed_password
