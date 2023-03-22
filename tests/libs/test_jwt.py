import pytest

from main.libs import jwt

# this token is expired
token = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJ1aWQiOjIyLCJleHAiOjE2Nzg5NDUxMzJ9."
    "ASkxTFCUR5RNv3764qoYVO8agrzWJD__ovZgf4m2tYY"
)


def test_extract_token_from_header():
    header = f"Bearer {token}"
    extracted_token = jwt.extract_jwt_from_header(header)
    assert extracted_token == token


def test_verify_invalid_token():
    with pytest.raises(Exception):
        jwt.verify_access_token(token)

    with pytest.raises(Exception):
        jwt.verify_access_token("123456")


def test_verify_token():
    token = jwt.create_access_token(100)
    payload = jwt.verify_access_token(token)
    assert payload["sub"] == 100
