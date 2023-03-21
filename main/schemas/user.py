from marshmallow import fields, validate

from main import config

from .base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Regexp(
            config.PATTERN_PWD,
            error="Passwords must have at least 6 characters, including "
            "at least one lowercase letter, one uppercase letter, one digit.",
        ),
    )
