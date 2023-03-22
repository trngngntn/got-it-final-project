import re

from main.commons import const
from main.libs import passwordlib

PATTERN_SALT = f"^[0-9a-f]{{{const.SALT_HEX_LEN}}}$"
PATTERN_HASH = f"^[0-9a-f]{{{const.HASHED_PASSWORD_LEN}}}$"


def test_salt_generator():
    assert re.match(PATTERN_SALT, passwordlib.generate_salt())


def test_password_hash():
    password = "qwe123rty456"
    salt = passwordlib.generate_salt()
    hashed_password = passwordlib.hash(password, salt)

    assert hashed_password != password
    assert re.match(PATTERN_HASH, hashed_password)
    assert passwordlib.verify_password(password, hashed_password, salt)
