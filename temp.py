import os
import random
from hashlib import pbkdf2_hmac

from main import db
from main.commons.exceptions import BadRequest
from main.libs import hash
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.schemas.exceptions import ErrorSchema


class TestErr(BadRequest):
    error_code = 2324
    error_data = {"key": "value"}

    # def __init__(self):
    #     # self.error_data = {"key": "value"}
    #     pass

    def js(self):
        return ErrorSchema().dumps(self)


HASH_ITERS = 100_000

salt = os.urandom(8)
print(salt.hex())
dk = pbkdf2_hmac("sha256", b"password", salt, HASH_ITERS)
dk_t = pbkdf2_hmac("sha256", b"password", bytes.fromhex(salt.hex()), HASH_ITERS)
print(dk.hex())
print(dk_t.hex())

print(TestErr().js())


def create_users():
    users = []
    print("CRERERRER")
    for i in range(0, 10):
        salt = hash.generate_salt()
        user = UserModel(
            email=f"user{i}@gmail.com",
            salt=salt,
            password=hash.hash_password("Abc123", salt),
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
                name=f"item #{category.id}{i}",
                description="this is an item",
                user_id=create_users[random.randint(0, 9)].id,
                category_id=category.id,
            )
            db.session.add(item)
    db.session.commit()
    return items
