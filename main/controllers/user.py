import os
from hashlib import pbkdf2_hmac

from flask import abort, make_response, request

import main.commons.http_status as HTTPStatus
from main import app, db
from main.commons import params
from main.commons.exceptions import DuplicatedEmailError
from main.libs import jwt
from main.libs.log import ServiceLogger
from main.models.user import UserModel
from main.schemas.user import UserSchema


def generate_salt() -> str:
    return os.urandom(params.SALT_BYTE_LENGTH).hex()


def hash_password(password: str, salt: str) -> str:
    return pbkdf2_hmac(
        params.HASH_ALGO, password.encode(), bytes.fromhex(salt), params.HASH_ITERS
    ).hex()


@app.post("/register")
def register():
    data = UserSchema().loads(request.get_data())

    if UserModel.query_by_email(data["email"]):
        raise DuplicatedEmailError()

    salt = generate_salt()
    user = UserModel(
        email=data["email"],
        salt=salt,
        password=hash_password(data["password"], salt),
    )
    db.session.add(user)
    db.session.commit()
    ServiceLogger(__name__).info(message=f"New user registered (id={user.id}).")
    token = jwt.create_access_token(user)
    return make_response({"access_token": token}, HTTPStatus.CREATED)


@app.post("/login")
def login():
    data = UserSchema().loads(request.get_data())
    user = UserModel.query_by_email(data["email"])

    if user and user.password == hash_password(data["password"], user.salt):
        ServiceLogger(__name__).info(message=f"User(id={user.id}) logged in.")
        token = jwt.create_access_token(user)
        return make_response({"access_token": token}, HTTPStatus.OK)

    abort(401)


# @app.get("/dump")
# @jwt.protect
# def dump_jwt(jwt):
#     return jwt
