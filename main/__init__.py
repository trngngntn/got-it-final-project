import sys
from importlib import import_module
from pathlib import Path

from alembic.command import upgrade
from alembic.config import Config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ._config import config
from .commons.error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa


register_subpackages()
register_error_handlers(app)


ALEMBIC_CONFIG = (
    (Path(__file__) / ".." / ".." / "migrations" / "alembic.ini").resolve().as_posix()
)


def refresh_db():
    db.reflect()
    db.drop_all()
    _config = Config(ALEMBIC_CONFIG)
    upgrade(_config, "heads")


with app.app_context():
    if "fresh-db" in sys.argv:
        refresh_db()

    if "sample-db" in sys.argv:
        import random
        import sys

        from main.libs import passwordlib
        from main.models.category import CategoryModel
        from main.models.item import ItemModel
        from main.models.user import UserModel

        def create_users():
            users = []
            for i in range(0, 10):
                salt = passwordlib.generate_salt()
                user = UserModel(
                    email=f"user{i}@gmail.com",
                    salt=salt,
                    password=passwordlib.hash("Abc123", salt),
                )
                db.session.add(user)
                db.session.flush()
                users.append(user)
            db.session.commit()
            return users

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

        def create_items(create_users, create_categories):
            items = []
            for category in create_categories:
                for i in range(0, random.randint(10, 50)):
                    item = ItemModel(
                        name=f"item #{category.id}_{i}",
                        description="this is an item",
                        user_id=create_users[random.randint(0, 9)].id,
                        category_id=category.id,
                    )
                    db.session.add(item)
            db.session.commit()
            return items

        refresh_db()
        users = create_users()
        create_items(users, create_categories(users))
