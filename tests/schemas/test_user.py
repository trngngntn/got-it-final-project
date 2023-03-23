import pytest
from marshmallow import ValidationError

from main.schemas.user import UserSchema


def test_load_schema():
    input_data = {
        "email": "abcd@abc.com",
        "password": "Qwe12323wd",
    }
    category = UserSchema().load(input_data)
    assert category == input_data


def test_load_schema_with_invalid_fields():
    input_data = {
        "email": "abcd@abc.com",
        "password": "123456789N",
    }
    with pytest.raises(ValidationError):
        UserSchema().load(input_data)

    input_data = {
        "email": "abcdasdasdasd",
        "password": "Bcd324324",
    }
    with pytest.raises(ValidationError):
        UserSchema().load(input_data)


def test_load_schema_with_missing_fields():
    input_data = {
        "email": "abcd@abc.com",
    }
    with pytest.raises(ValidationError):
        UserSchema().load(input_data)

    input_data = {
        "password": "Abcdcd23423",
    }
    with pytest.raises(ValidationError):
        UserSchema().load(input_data)
