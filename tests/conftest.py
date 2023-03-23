import os
import random
import sys
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config

from main import app as _app
from main import db
from main.libs import password as password_lib
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel

if os.getenv("ENVIRONMENT") != "test":
    print('Tests should be run with "ENVIRONMENT=test"')
    sys.exit(1)

ALEMBIC_CONFIG = (
    (Path(__file__) / ".." / ".." / "migrations" / "alembic.ini").resolve().as_posix()
)


@pytest.fixture(scope="session", autouse=True)
def app():
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session", autouse=True)
def recreate_database(app):
    db.reflect()
    db.drop_all()
    _config = Config(ALEMBIC_CONFIG)
    upgrade(_config, "heads")


@pytest.fixture(scope="function", autouse=True)
def session(recreate_database):
    from sqlalchemy.orm import sessionmaker

    connection = db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    session = db.scoped_session(session_factory)

    db.session = session

    yield

    transaction.rollback()
    connection.close()
    session.close()


@pytest.fixture(scope="function", autouse=True)
def client(app, session):
    return app.test_client()


@pytest.fixture()
def users():
    users = []
    for i in range(0, 10):
        salt = password_lib.generate_salt()
        user = UserModel(
            email=f"user{i}@gmail.com",
            salt=salt,
            password=password_lib.hash_password("Abc123", salt),
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users


@pytest.fixture()
def login_users(client, users):
    user_tokens = []
    for user in users:
        response = client.post(
            "/login",
            json={"email": user.email, "password": "Abc123"},
        )
        user_tokens.append(response.json["access_token"])
    return user_tokens


@pytest.fixture()
def categories(users):
    categories = []
    for i in range(0, 50):
        category = CategoryModel(
            name=f"category #{i}",
            user_id=users[random.randint(0, 9)].id,
        )
        db.session.add(category)
        categories.append(category)
    db.session.commit()
    return categories


@pytest.fixture()
def items(users, categories):
    items = []
    for category in categories:
        for i in range(0, random.randint(10, 50)):
            item = ItemModel(
                name=f"item #{category.id}_{i}",
                description="this is an item",
                user_id=users[random.randint(0, 9)].id,
                category_id=category.id,
            )
            db.session.add(item)
            items.append(item)
    db.session.commit()
    return items
