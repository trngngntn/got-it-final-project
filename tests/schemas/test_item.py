import pytest

from main.schemas.item import ItemSchema, ItemUpdateSchema


def test_load_schema():
    input_data = {
        "name": "item_name",
        "description": "item_description",
    }
    category = ItemSchema().load(input_data)
    assert category == input_data


def test_load_schema_with_long_name():
    input_data = {
        "name": "123456789012345678901234567890123456789012345678901234567890",
    }
    with pytest.raises(Exception):
        ItemSchema().load(input_data)


def test_load_schema_with_missing_fields():
    input_data = {
        "name": "abc",
    }
    with pytest.raises(Exception):
        ItemSchema().load(input_data)
    input_data = {
        "description": "abc",
    }
    with pytest.raises(Exception):
        ItemSchema().load(input_data)


def test_load_update_schema():
    input_data = {"name": "abc"}
    item = ItemUpdateSchema().load(input_data)
    assert item == input_data
    input_data = {"description": "abc"}
    item = ItemUpdateSchema().load(input_data)
    assert item == input_data


def test_load_update_schema_with_all_fields_missing():
    input_data = {}
    with pytest.raises(Exception):
        ItemUpdateSchema().load(input_data)
