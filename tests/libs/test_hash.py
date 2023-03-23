import re

import pytest

from main.commons import const
from main.libs import password as password_lib

PATTERN_SALT = f"^[0-9a-f]{{{const.SALT_HEX_LEN}}}$"
PATTERN_HASH = f"^[0-9a-f]{{{const.HASHED_PASSWORD_LEN}}}$"


def test_salt_generator():
    assert re.match(PATTERN_SALT, password_lib.generate_salt())


def test_password_hash():
    password = "qwe123rty456"
    salt = password_lib.generate_salt()
    hashed_password = password_lib.hash_password(password, salt)

    assert hashed_password != password
    assert re.match(PATTERN_HASH, hashed_password)
    assert password_lib.verify_password(password, hashed_password, salt)

    salt = "1234567890qwerty"
    with pytest.raises(ValueError):
        password_lib.hash_password(password, salt)
