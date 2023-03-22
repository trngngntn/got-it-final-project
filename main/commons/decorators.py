from functools import wraps

from flask import request

from main import db
from main.commons.exceptions import InvalidJWTError, Unauthorized
from main.libs.jwt import extract_jwt_from_header, verify_access_token
from main.libs.log import ServiceLogger
from main.models.item import ItemModel
from main.models.user import UserModel

logger = ServiceLogger(__name__)


def require_token(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Unauthorized()

        try:
            jwt_str = extract_jwt_from_header(auth_header)
            jwt_payload = verify_access_token(jwt_str)

            user = db.session.get(UserModel, jwt_payload["sub"])
            if user is None:
                raise Unauthorized()

            return func(*args, **kwargs, user=user)

        except InvalidJWTError:
            raise Unauthorized()

    return wrapped_func


def use_request_schema(schema):
    def wrapped_func(func):
        @wraps(func)
        def load_data(*args, **kwargs):
            if request.method in ["POST", "PUT"]:
                data = request.get_json()
            else:
                data = request.args
            data = schema.load(data)
            return func(*args, **kwargs, request_data=data)

        return load_data

    return wrapped_func


def get_item(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        category_id = kwargs.get("category_id")
        item_id = kwargs.get("item_id")
        item = ItemModel.query.filter(
            ItemModel.category_id == category_id, ItemModel.id == item_id
        ).first_or_404()
        return func(*args, **kwargs, item=item)

    return wrapped_func
