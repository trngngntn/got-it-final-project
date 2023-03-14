from base import BaseSchema
from marshmallow import fields


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
