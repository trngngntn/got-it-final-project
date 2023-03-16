import re
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from main.commons import params
from main.libs.log import ServiceLogger
from main.models.user import UserModel


def create_access_token(user: UserModel) -> str:
    payload = {}
    payload["uid"] = user.id
    payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(
        seconds=params.JWT_TIMEOUT_SECONDS
    )
    ServiceLogger(__name__).info(
        message=f"now={datetime.now(tz=timezone.utc)}, exp={payload['exp']},\
              delta={timedelta(seconds=params.JWT_TIMEOUT_SECONDS)}"
    )
    token = jwt.encode(payload, params.SECRET_KEY, algorithm=params.JWT_ALGO)
    return token


def verify_access_token(token: str) -> dict:
    payload = jwt.decode(token, params.SECRET_KEY, algorithms=params.JWT_ALGO)
    ServiceLogger(__name__).info(message=f"jwt_payload={payload}")
    return payload


def extract_jwt(header: str) -> str:
    match = re.fullmatch(params.PATTERN_HTTP_BEARER_AUTH, header)
    if not match:
        raise InvalidTokenError()
    return header[7:]
