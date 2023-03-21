from marshmallow import fields, validate

from .base import BaseSchema, PaginationSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    user_id = fields.Integer(dump_only=True)


class CategoryListSchema(PaginationSchema):
    data = fields.List(
        fields.Nested(CategorySchema),
        attribute="items",
        validate=validate.Length(max=20),
    )
