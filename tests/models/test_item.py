from main import db
from main.models.item import ItemModel


def test_model(items):
    category = db.session.get(ItemModel, items[0].id)
    assert category.name == items[0].name
