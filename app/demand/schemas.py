from marshmallow import Schema, fields

from app.account.schemas import UserSchema
from app.helpers import PublisherIDSchemaMixin


class MeetingDemandSchema(Schema, PublisherIDSchemaMixin):
    id = fields.Integer(dump_only=True)
    signaler = fields.Nested(UserSchema, dump_only=True)
    publisher = fields.Nested(UserSchema, dump_only=True)
    title = fields.Str(required=True)
    introduce = fields.Str(required=True)
    is_enabled = fields.Boolean(dump_only=True)
