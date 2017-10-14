from marshmallow import Schema, fields

from app.account.schemas import UserSchema
from app.helpers import PublisherIDSchemaMixin


class MeetingSchema(Schema, PublisherIDSchemaMixin):
    id = fields.Integer(dump_only=True)
    publisher = fields.Nested(UserSchema, dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    maximum_people = fields.Integer()
    location = fields.Str()
    entry_fee = fields.Integer()
    entry_fee_type = fields.Str()

    entry_due_time = fields.DateTime()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    created_time = fields.DateTime(dump_only=True)
