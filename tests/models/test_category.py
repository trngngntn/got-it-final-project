from main import db
from main.models.category import CategoryModel


def test_model(create_categories):
    category = db.session.get(CategoryModel, create_categories[0].id)
    assert category.name == create_categories[0].name
