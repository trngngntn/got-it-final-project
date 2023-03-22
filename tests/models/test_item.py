from main import db
from main.models.item import ItemModel


def test_model(create_items):
    category = db.session.get(ItemModel, create_items[0].id)
    assert category.name == create_items[0].name
