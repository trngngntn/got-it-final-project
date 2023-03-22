from marshmallow import ValidationError, fields, validate, validates_schema

from main import config
from main.commons import const

from .base import BaseSchema, PaginationSchema
from .fields.trimmed_string import TrimmedString


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = TrimmedString(
        required=True, validate=validate.Length(min=1, max=const.FIELD_NAME_MAX_LEN)
    )
    description = TrimmedString(
        required=True, validate=validate.Length(min=1, max=const.FIELD_DESC_MAX_LEN)
    )
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(dump_only=True)


class ItemListSchema(PaginationSchema):
    data = fields.List(
        fields.Nested(ItemSchema),
        attribute="items",
        validate=validate.Length(max=config.PAGINATION_MAX_ITEMS),
    )


class ItemUpdateSchema(BaseSchema):
    name = fields.String(validate=validate.Length(max=const.FIELD_NAME_MAX_LEN))
    description = fields.String(validate=validate.Length(max=const.FIELD_DESC_MAX_LEN))

    @validates_schema
    def required_at_least_one_field(self, data, **_):
        if not (data.get("name") or data.get("description")):
            raise ValidationError(
                "At least one of the fields 'name' or 'description' is required."
            )
