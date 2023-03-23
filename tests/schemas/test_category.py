import pytest
from marshmallow import ValidationError

from main.schemas.category import CategorySchema


def test_load_schema():
    input_data = {
        "name": "category_name",
    }
    category = CategorySchema().load(input_data)
    assert category == input_data


def test_load_schema_with_long_name():
    input_data = {
        "name": "123456789012345678901234567890123456789012345678901234567890",
    }
    with pytest.raises(ValidationError):
        CategorySchema().load(input_data)


def test_load_schema_with_no_name():
    input_data = {
        "not_name": "abc",
    }
    with pytest.raises(ValidationError):
        CategorySchema().load(input_data)
