from marshmallow import ValidationError, fields, validate, validates_schema

from .base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    description = fields.String(required=True)
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(dump_only=True)


class ItemUpdateSchema(BaseSchema):
    name = fields.String(required=False, validate=validate.Length(max=50))
    description = fields.String(required=False)

    @validates_schema
    def required_at_least_one_field(self, data, **kwargs):
        if not (data.get("name") or data.get("description")):
            raise ValidationError(
                "At least one of the fields 'name' or 'description' is required."
            )
