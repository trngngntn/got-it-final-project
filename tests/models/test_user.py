from main import db
from main.models.user import UserModel


def test_model(users):
    category = db.session.get(UserModel, users[0].id)
    assert category.email == users[0].email
