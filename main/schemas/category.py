from marshmallow import fields, validate

from .base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    user_id = fields.Integer(dump_only=True)
