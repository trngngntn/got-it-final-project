from typing import Optional

from flask import make_response

from main.schemas.exceptions import ErrorSchema


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class _ErrorCode:
    BAD_REQUEST = 400000
    VALIDATION_ERROR = 400001
    UNAUTHORIZED = 401000
    FORBIDDEN = 403000
    NOT_FOUND = 404000
    METHOD_NOT_ALLOWED = 405000
    CONFLICT = 409000
    DUPLICATED_USER_EMAIL = 409001
    DUPLICATED_CATEGORY_NAME = 409002
    DUPLICATED_ITEM_NAME = 409003
    INTERNAL_SERVER_ERROR = 500000


class _ErrorMessage:
    BAD_REQUEST = "Bad request."
    VALIDATION_ERROR = "Validation error."
    UNAUTHORIZED = "Unauthorized."
    FORBIDDEN = "Forbidden."
    NOT_FOUND = "Not found."
    METHOD_NOT_ALLOWED = "Method not allowed."
    CONFLICT = "Conflict."
    DUPLICATED_USER_EMAIL = "An user with the same e-mail is already existed."
    DUPLICATED_CATEGORY_NAME = "A category with the same name is already existed."
    DUPLICATED_ITEM_NAME = "An item with the same name is already existed."
    INTERNAL_SERVER_ERROR = "Internal server error."


class BaseError(Exception):
    def __init__(
        self,
        *,
        error_message=None,
        error_data=None,
        status_code: Optional[int] = None,
        error_code: Optional[int] = None,
    ):
        """
        Customize the response exception

        :param error_message: <string> Message field in the response body
        :param status_code: <number> HTTP status code
        :param error_data: <dict> Json body data
        :param error_code: <number> error code
        """
        if error_message is not None:
            self.error_message = error_message

        if status_code is not None:
            self.status_code = status_code

        if error_code is not None:
            self.error_code = error_code

        self.error_data = error_data

    def to_dict(self):
        return {
            "error_code": self.error_code,
            "error_data": self.error_data,
            "error_message": self.error_message,
        }

    def to_response(self):
        response = ErrorSchema().jsonify(self)

        return make_response(response, self.status_code)


# add invalid token error
class BadRequest(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.BAD_REQUEST
    error_code = _ErrorCode.BAD_REQUEST


class ValidationError(BaseError):
    status_code = StatusCode.BAD_REQUEST
    error_message = _ErrorMessage.VALIDATION_ERROR
    error_code = _ErrorCode.VALIDATION_ERROR


class Unauthorized(BaseError):
    status_code = StatusCode.UNAUTHORIZED
    error_message = _ErrorMessage.UNAUTHORIZED
    error_code = _ErrorCode.UNAUTHORIZED


class Forbidden(BaseError):
    status_code = StatusCode.FORBIDDEN
    error_message = _ErrorMessage.FORBIDDEN
    error_code = _ErrorCode.FORBIDDEN


class NotFound(BaseError):
    status_code = StatusCode.NOT_FOUND
    error_message = _ErrorMessage.NOT_FOUND
    error_code = _ErrorCode.NOT_FOUND


class MethodNotAllowed(BaseError):
    status_code = StatusCode.METHOD_NOT_ALLOWED
    error_message = _ErrorMessage.METHOD_NOT_ALLOWED
    error_code = _ErrorCode.METHOD_NOT_ALLOWED


class InternalServerError(BaseError):
    status_code = StatusCode.INTERNAL_SERVER_ERROR
    error_message = _ErrorMessage.INTERNAL_SERVER_ERROR
    error_code = _ErrorCode.INTERNAL_SERVER_ERROR


class ConflictError(BaseError):
    status_code = StatusCode.CONFLICT
    error_message = _ErrorMessage.CONFLICT
    error_code = _ErrorCode.CONFLICT


class DuplicatedEmailError(ConflictError):
    error_message = _ErrorMessage.DUPLICATED_USER_EMAIL
    error_code = _ErrorCode.DUPLICATED_USER_EMAIL


class DuplicatedCategoryNameError(ConflictError):
    error_message = _ErrorMessage.DUPLICATED_CATEGORY_NAME
    error_code = _ErrorCode.DUPLICATED_CATEGORY_NAME


class DuplicatedItemNameError(ConflictError):
    error_message = _ErrorMessage.DUPLICATED_ITEM_NAME
    error_code = _ErrorCode.DUPLICATED_ITEM_NAME


class InvalidJWTError(Exception):
    pass
