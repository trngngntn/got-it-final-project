import pytest


class ErrorResponse:
    # TODO: remove, import from commons
    def __init__(self, error_code, error_message):
        self.msg_dict = {"error_code": error_code, "error_message": error_message}
        if error_code != 400001:
            self.msg_dict["error_data"] = None


@pytest.fixture()
def response_bad_request():
    return ErrorResponse(400000, "Bad request.").msg_dict


@pytest.fixture()
def response_validation_error():
    return ErrorResponse(400001, "Validation error.").msg_dict


@pytest.fixture()
def response_unauthorized():
    return ErrorResponse(401000, "Unauthorized.").msg_dict


@pytest.fixture()
def response_forbidden():
    return ErrorResponse(403000, "Forbidden.").msg_dict


@pytest.fixture()
def response_not_found():
    return ErrorResponse(404000, "Not found.").msg_dict
