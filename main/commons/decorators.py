from functools import wraps

from flask import abort, request
from jwt.exceptions import InvalidTokenError

from main.commons import http_status as HTTPStatus
from main.commons.exceptions import Unauthorized
from main.libs.jwt import extract_jwt, verify_access_token
from main.libs.log import ServiceLogger


def require_token(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Unauthorized()
        try:
            jwt_str = extract_jwt(auth_header)
            jwt_payload = verify_access_token(jwt_str)
            return func(*args, **kwargs, jwt=jwt_payload)
        except InvalidTokenError:
            ServiceLogger(__name__).warning(message="Invalid token.")
            abort(HTTPStatus.UNAUTHORIZED)

    return wrapped_func


def paginate(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            page = request.args.get("page")
            if page is None:
                page = 1
            else:
                page = int(request.args.get("page"))
                if page < 1:
                    abort(HTTPStatus.NOT_FOUND)
        except ValueError:
            abort(HTTPStatus.BAD_REQUEST)
        return func(*args, **kwargs, page=page)

    return wrapped_func


# def validate_path_variables(var_name, var_type):
#     def wrapped_func(func):
#         @wraps(func)
#         def validate_vars(*args, **kwargs):
#             ServiceLogger(__name__).info(message=f"var={var_name}")
#             if kwargs.get(var_name) is not var_type:
#                 abort(HTTPStatus.BAD_REQUEST)
#             return func(*args, **kwargs)
#         return validate_vars
#     return wrapped_func
