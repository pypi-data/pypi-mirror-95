from dataclasses import dataclass
from pathlib import Path

from datamx.models.values import BaseSchema
from marshmallow import fields, post_load, ValidationError


class PathField(fields.Field):
    """Field that serializes to a string
        deserializes to a Path.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return Path(value)
        except ValueError as error:
            raise ValidationError("PathField must be a string") from error


@dataclass
class ConnectOptions:
    device_type: str
    slave_id: int = 1
    name: str = None
    pathlist: str = None
    baudrate: str = None
    parity: str = None
    ip_address: str = None
    ip_port: str = None
    timeout: str = None
    trace: str = None
    scan_progress: str = None
    scan_delay: str = None

class ConnectOptionsSchema(BaseSchema):
    device_type = fields.String()
    slave_id = fields.Integer()
    name = fields.String()
    pathlist = fields.String()
    baudrate = fields.Integer()
    parity = fields.String()
    ip_address = fields.String()
    ip_port = fields.Integer()
    timeout = fields.Float()
    trace = fields.Boolean()
    scan_progress = fields.Boolean()
    scan_delay = fields.Float()

    @post_load
    def make_request(self, data, **kwargs):
        return ConnectOptions(**data)


class ReadOptions:

    def __init__(self, include_models=None, exclude_models=None, include_ids=None, exclude_ids=None, output_path=None):
        self.include_models = ReadOptions.empty_if_not_set(include_models)
        self.exclude_models = ReadOptions.empty_if_not_set(exclude_models)
        self.include_ids = ReadOptions.empty_if_not_set(include_ids)
        self.exclude_ids = ReadOptions.empty_if_not_set(exclude_ids)
        self.output_path = output_path

    def add_include_id(self, id):
        self.include_ids.append(id)

    def add_exclude_id(self, id):
        self.exclude_ids.append(id)

    def add_include_model(self, id):
        self.include_models.append(id)

    def add_exclude_model(self, id):
        self.exclude_models.append(id)

    def allow_id(self, id):
        return ReadOptions._allow(id, self.include_ids, self.exclude_ids)

    def allow_model(self, id):
        return ReadOptions._allow(id, self.include_models, self.exclude_models)

    @staticmethod
    def _allow(key, includes, excludes):
        if includes:
            return key in includes
        elif excludes:
            return key not in excludes
        else:
            return True

    @staticmethod
    def empty_if_not_set(include_models):
        return include_models if include_models else []


class ReadOptionsSchema(BaseSchema):
    include_models = fields.List(fields.String())
    exclude_models = fields.List(fields.String())
    include_ids = fields.List(fields.String())
    exclude_ids = fields.List(fields.String())
    output_path = PathField()

    @post_load
    def make_request(self, data, **kwargs):
        return ReadOptions(**data)
