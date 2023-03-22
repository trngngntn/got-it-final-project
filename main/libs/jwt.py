from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from main import config
from main.commons import const
from main.commons.exceptions import InvalidJWTError
from main.libs.log import ServiceLogger
from main.models.user import UserModel

logger = ServiceLogger(__name__)


# TODO: input model -> input user id only
def create_access_token(user: UserModel) -> str:
    payload = {
        "sub": user.id,
        "exp": datetime.now(tz=timezone.utc)
        + timedelta(seconds=config.JWT_TIMEOUT_SECONDS),
    }
    token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=const.JWT_ALGO)
    return token


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[const.JWT_ALGO])
    except InvalidTokenError:
        raise InvalidJWTError()

    return payload


def extract_jwt_from_header(header: str) -> str:
    if header.startswith("Bearer "):
        return header.split(" ")[1]

    raise InvalidJWTError()
