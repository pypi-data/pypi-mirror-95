from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Any

from marshmallow import Schema, fields, post_load, post_dump


class BaseSchema(Schema):
    # SKIP_VALUES = {None}

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            # if value not in BaseSchema.SKIP_VALUES
            if value is not None
        }


@dataclass
class Value:
    id: str = None
    value: Any = None


class ValueSchema(BaseSchema):
    id = fields.String()
    value = fields.Raw()

    @post_load
    def make_request(self, data, **kwargs):
        return Value(**data)


@dataclass
class Group:
    name: str = None
    type: str = None
    values: List[Value] = field(default_factory=list)


class GroupSchema(BaseSchema):
    name = fields.String()
    type = fields.String()
    values = fields.List(fields.Nested(ValueSchema))

    @post_load
    def make_request(self, data, **kwargs):
        return Group(**data)


@dataclass
class Groups:
    datetime: datetime = None
    groups: List[Group] = field(default_factory=list)


class GroupsSchema(BaseSchema):
    datetime = fields.NaiveDateTime()
    groups = fields.List(fields.Nested(GroupSchema))

    @post_load
    def make_request(self, data, **kwargs):
        return Groups(**data)
