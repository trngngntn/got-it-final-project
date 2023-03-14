from base import BaseSchema
from marshmallow import fields


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    user_id = fields.Integer(dump_only=True)
