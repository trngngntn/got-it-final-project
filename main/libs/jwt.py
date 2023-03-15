import re
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import request

from main.commons import params
from main.commons.exceptions import Unauthorized
from main.libs.log import ServiceLogger
from main.models.user import UserModel


def create_access_token(user: UserModel) -> str:
    payload = {}
    payload["uid"] = user.id
    payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(
        seconds=params.JWT_TIMEOUT_SECONDS
    )
    ServiceLogger("jwt").info(
        message=f"now={datetime.now(tz=timezone.utc)}, exp={payload['exp']},\
              delta={timedelta(seconds=params.JWT_TIMEOUT_SECONDS)}"
    )
    token = jwt.encode(payload, params.SECRET_KEY, algorithm=params.JWT_ALGO)
    return token


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, params.SECRET_KEY, algorithms=params.JWT_ALGO)
    except jwt.exceptions.InvalidTokenError as e:
        raise Unauthorized(error_message=e)
    ServiceLogger("jwt").info(message=f"jwt_payload={payload}")
    return payload


def extract_jwt(header: str) -> str:
    match = re.fullmatch("^Bearer ([A-Za-z0-9_-]+\\.){2}[A-Za-z0-9_-]*$", header)
    if match:
        return header[7:]
    raise Unauthorized()


def protect(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Unauthorized()
        jwt_str = extract_jwt(auth_header)
        jwt_payload = verify_access_token(jwt_str)
        ServiceLogger("jwt").info(message=f"jwt={jwt_str}")
        return func(*args, **kwargs, jwt=jwt_payload)

    return wrapped_func
