from base import BaseSchema
from marshmallow import fields


class ItemSchema(BaseSchema):
    id: fields.Integer(dump_only=True)
    name: fields.String(required=True)
    description: fields.String(required=True)
    user_id: fields.Integer(dump_only=True)
    category_id: fields.Integer(dump_only=True)
