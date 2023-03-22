from main import db
from main.models.user import UserModel


def test_model(create_users):
    category = db.session.get(UserModel, create_users[0].id)
    assert category.email == create_users[0].email
