from flask import make_response

import main.commons.http_status as HTTPStatus
from main import app, db
from main.commons.decorators import response_schema
from main.commons.exceptions import DuplicatedEmailError, Unauthorized
from main.libs import hash, jwt
from main.libs.log import ServiceLogger
from main.models.user import UserModel
from main.schemas.user import UserSchema

logger = ServiceLogger(__name__)


@app.post("/register")
@response_schema(UserSchema)
def register(email, password):
    if UserModel.query_by_email(email):
        raise DuplicatedEmailError()

    salt = hash.generate_salt()
    user = UserModel(
        email=email,
        salt=salt,
        password=hash.hash_password(password, salt),
    )

    db.session.add(user)
    db.session.commit()

    logger.info(message=f"New user registered (id={user.id}).")
    token = jwt.create_access_token(user)

    return make_response({"access_token": token}, HTTPStatus.CREATED)


@app.post("/login")
@response_schema(UserSchema)
def login(email, password):
    user = UserModel.query_by_email(email)

    if user and hash.verify_password(password, user.password, user.salt):
        logger.info(message=f"User(id={user.id}) logged in.")
        token = jwt.create_access_token(user)
        return make_response({"access_token": token})

    raise Unauthorized()
