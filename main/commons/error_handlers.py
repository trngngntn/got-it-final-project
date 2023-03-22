import json

from marshmallow import exceptions as marshmallow_exceptions
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

logger = ServiceLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(json.decoder.JSONDecodeError)
    @app.errorhandler(exceptions.BadRequest)
    @app.errorhandler(400)
    def handle_bad_request(e):
        logger.warning(message=e)
        return BadRequest().to_response()

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
        logger.exception(message=str(e))

        return InternalServerError(error_message=str(e)).to_response()

    @app.errorhandler(marshmallow_exceptions.ValidationError)
    def handle_validation_error(e):
        return ValidationError(error_data=e.messages_dict).to_response()
