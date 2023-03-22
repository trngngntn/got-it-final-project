from flask import make_response

from main import app, db
from main.commons.decorators import use_request_schema
from main.commons.exceptions import DuplicatedEmailError, Unauthorized
from main.libs import jwt, passwordlib
from main.libs.log import ServiceLogger
from main.models.user import UserModel
from main.schemas.user import UserSchema

logger = ServiceLogger(__name__)


@app.post("/register")
@use_request_schema(UserSchema)
def register(request_data):
    email = request_data.get("email")
    password = request_data.get("password")

    if UserModel.query_by_email(email):
        raise DuplicatedEmailError()

    salt = passwordlib.generate_salt()
    user = UserModel(
        email=email,
        salt=salt,
        password=passwordlib.hash(password, salt),
    )

    db.session.add(user)
    db.session.commit()

    logger.info(message=f"New user registered (id={user.id}).")
    token = jwt.create_access_token(user)

    return make_response({"access_token": token}, 201)


@app.post("/login")
@use_request_schema(UserSchema)
def login(request_data):
    email = request_data.get("email")
    password = request_data.get("password")

    user = UserModel.query_by_email(email)

    if user and passwordlib.verify_password(password, user.password, user.salt):
        logger.info(message=f"User(id={user.id}) logged in.")
        token = jwt.create_access_token(user)
        return make_response({"access_token": token})

    raise Unauthorized()
