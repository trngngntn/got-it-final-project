import json

import jwt
from marshmallow import exceptions as mm_exceptions
from werkzeug import exceptions

from main.libs.log import ServiceLogger

from .exceptions import (
    BadRequest,
    BaseError,
    Forbidden,
    InternalServerError,
    MethodNotAllowed,
    NotFound,
    StatusCode,
    Unauthorized,
    ValidationError,
)


def register_error_handlers(app):
    @app.errorhandler(json.decoder.JSONDecodeError)
    @app.errorhandler(exceptions.BadRequest)
    @app.errorhandler(400)
    def handle_bad_request(e):
        ServiceLogger(__name__).warning(message=e)
        return BadRequest().to_response()

    @app.errorhandler(jwt.exceptions.InvalidTokenError)
    @app.errorhandler(401)
    def unauthorized(_):
        return Unauthorized().to_response()

    @app.errorhandler(403)
    def forbidden(_):
        return Forbidden().to_response()

    @app.errorhandler(404)
    def not_found(_):
        return NotFound().to_response()

    @app.errorhandler(405)
    def not_allowed(_):
        return MethodNotAllowed().to_response()

    @app.errorhandler(BaseError)
    def handle_error(error: BaseError):
        from main.libs.log import ServiceLogger

        logger = ServiceLogger(__name__)

        status_code = error.status_code
        if (
            isinstance(status_code, int)
            and status_code != StatusCode.INTERNAL_SERVER_ERROR
        ):
            logging_method = logger.warning
        else:
            logging_method = logger.error

        logging_method(
            message=error.error_message,
            data={
                "error_data": error.error_data,
                "error_code": error.error_code,
            },
        )
        return error.to_response()

    @app.errorhandler(Exception)
    def handle_exception(e):
        from main.libs.log import ServiceLogger

        logger = ServiceLogger(__name__)
        logger.exception(message=str(e))

        return InternalServerError(error_message=str(e)).to_response()

    @app.errorhandler(mm_exceptions.ValidationError)
    def handle_validation_error(e):
        return ValidationError(error_data=str(e)).to_response()
