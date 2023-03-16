from flask import jsonify
from flask_sqlalchemy.pagination import Pagination
from marshmallow import EXCLUDE, Schema, fields, pre_dump


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))

    # @pre_dump(pass_many=True)
    # def include_paginate(self, data, many, **kwargs):
    #     ServiceLogger(__name__).info(message=f"Predump {self.__name__}")

    #     return data

    # @post_dump(pass_many=True)
    # def wrap(self, data, many, **kwargs):
    #     wrapped_data = kwargs["pagination"]
    #     wrapped_data["data"] = data
    #     return wrapped_data


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()


def make_pagination_schema(cls: BaseSchema):
    class DataWrappedPaginationSchema(PaginationSchema):
        data = fields.List(fields.Nested(cls))

        @pre_dump
        def remap_fields(self, data, many, **kwargs):
            if isinstance(data, Pagination):
                data.items_per_page = data.per_page
                data.total_items = data.total
                data.data = data.items
            return data

    return DataWrappedPaginationSchema()
