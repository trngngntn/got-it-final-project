import os
from hashlib import pbkdf2_hmac

from flask import abort, request

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
    user_credentials = UserSchema().loads(request.get_data())

    if UserModel.query.filter(UserModel.email == user_credentials["email"]).first():
        raise DuplicatedEmailError()

    salt = generate_salt()
    user = UserModel(
        email=user_credentials["email"],
        salt=salt,
        password=hash_password(user_credentials["password"], salt),
    )
    db.session.add(user)
    db.session.commit()
    ServiceLogger("user_controller").info(
        message=f"New user registered (id={user.id})."
    )
    jws = jwt.create_access_token(user)
    return {"access_token": jws}


@app.post("/login")
def login():
    user_credentials = UserSchema().loads(request.get_data())
    user = UserModel.query.filter(UserModel.email == user_credentials["email"]).first()

    if user and user.password == hash_password(user_credentials["password"], user.salt):
        ServiceLogger("user_controller").info(message=f"User(id={user.id}) logged in.")
        jws = jwt.create_access_token(user)
        return {"access_token": jws}

    abort(401)


@app.get("/dump")
@jwt.protect
def dump_jwt(jwt):
    return jwt
