from main import db
from main.models.category import CategoryModel


def test_model(categories):
    category = db.session.get(CategoryModel, categories[0].id)
    assert category.name == categories[0].name
