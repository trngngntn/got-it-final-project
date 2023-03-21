import re

from main.libs import hash

PATTERN_SALT = "^[0-9a-f]{16}$"
PATTERN_HASH = "^[0-9a-f]{64}$"


def test_salt_generator():
    assert re.match(PATTERN_SALT, hash.generate_salt())


def test_password_hash():
    password = "qwe123rty456"
    salt = hash.generate_salt()
    hashed_password = hash.hash_password(password, salt)
    assert hashed_password != password
    assert re.match(PATTERN_HASH, hashed_password)
    assert hash.verify_password(password, hashed_password, salt)
