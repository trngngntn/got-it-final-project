from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields, validate


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer(attribute="per_page")
    page = fields.Integer()
    total_items = fields.Integer(attribute="total")


class ParamPageSchema(BaseSchema):
    page = fields.Integer(missing=1, range=validate.Range(min=1))
