from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from main import config
from main.libs.log import ServiceLogger
from main.models.user import UserModel


def create_access_token(user: UserModel) -> str:
    payload = {
        "sub": user.id,
        "exp": datetime.now(tz=timezone.utc)
        + timedelta(seconds=config.JWT_TIMEOUT_SECONDS),
    }
    ServiceLogger(__name__).info(
        message=f"now={datetime.now(tz=timezone.utc)}, exp={payload['exp']},\
              delta={timedelta(seconds=config.JWT_TIMEOUT_SECONDS)}"
    )
    token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGO)
    return token


def verify_access_token(token: str) -> dict:
    payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGO])
    ServiceLogger(__name__).info(message=f"jwt_payload={payload}")
    return payload


def extract_jwt_from_header(header: str) -> str:
    if header.startswith("Bearer "):
        return header[7:]
    raise InvalidTokenError()
