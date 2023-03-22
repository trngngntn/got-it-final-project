import typing

from marshmallow import fields


class TrimmedString(fields.String):
    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if hasattr(value, "strip"):
            value = value.strip()
        return super()._deserialize(value, attr, data, **kwargs)
