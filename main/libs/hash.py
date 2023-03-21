import os
from hashlib import pbkdf2_hmac

from main import config


def generate_salt() -> str:
    return os.urandom(config.SALT_BYTE_LENGTH).hex()


def hash_password(password: str, salt: str) -> str:
    return pbkdf2_hmac(
        config.HASH_ALGO, password.encode(), bytes.fromhex(salt), config.HASH_ITERS
    ).hex()


def verify_password(password: str, hashed_password: str, salt: str):
    return hash_password(password, salt) == hashed_password  # use a function to compare
