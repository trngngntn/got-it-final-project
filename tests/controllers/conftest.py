import random

import pytest

from main import db
from main.libs import hash
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


@pytest.fixture()
def create_users():
    users = []
    for i in range(0, 10):
        salt = hash.generate_salt()
        user = UserModel(
            email=f"user{i}@gmail.com",
            salt=salt,
            password=hash.hash_password("Abc123", salt),
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users


@pytest.fixture()
def login_users(client, create_users):
    user_tokens = []
    for user in create_users:
        response = client.post(
            "/login",
            json={"email": user.email, "password": "Abc123"},
        )
        user_tokens.append(response.json["access_token"])
    return user_tokens


@pytest.fixture()
def create_categories(create_users):
    categories = []
    for i in range(0, 50):
        category = CategoryModel(
            name=f"category #{i}",
            user_id=create_users[random.randint(0, 9)].id,
        )
        db.session.add(category)
        categories.append(category)
    db.session.commit()
    return categories


@pytest.fixture()
def create_items(create_users, create_categories):
    items = []
    for category in create_categories:
        for i in range(0, random.randint(10, 50)):
            item = ItemModel(
                name=f"item #{category.id}{i}",
                description="this is an item",
                user_id=create_users[random.randint(0, 9)].id,
                category_id=category.id,
            )
            db.session.add(item)
            items.append(item)
    db.session.commit()
    return items


class ErrorResponse:
    def __init__(self, error_code, error_message):
        self.msg_dict = {"error_code": error_code, "error_message": error_message}
        if error_code != 400001:
            self.msg_dict["error_data"] = None


@pytest.fixture()
def response_bad_request():
    return ErrorResponse(400000, "Bad request.").msg_dict


@pytest.fixture()
def response_validation_error():
    return ErrorResponse(400001, "Validation error.").msg_dict


@pytest.fixture()
def response_unauthorized():
    return ErrorResponse(401000, "Unauthorized.").msg_dict


@pytest.fixture()
def response_forbidden():
    return ErrorResponse(403000, "Forbidden.").msg_dict


@pytest.fixture()
def response_not_found():
    return ErrorResponse(404000, "Not found.").msg_dict
