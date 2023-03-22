from marshmallow import fields, validate

from .base import BaseSchema, PaginationSchema
from .fields.trimmed_string import TrimmedString


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = TrimmedString(required=True, validate=validate.Length(min=1, max=50))
    user_id = fields.Integer(dump_only=True)


class CategoryListSchema(PaginationSchema):
    data = fields.List(
        fields.Nested(CategorySchema),
        attribute="items",
        validate=validate.Length(max=20),
    )
