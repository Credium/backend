from flask import g
from marshmallow import Schema, ValidationError, fields, validates

from app.account.schemas import UserSchema
from app.helpers import PublisherIDSchemaMixin

from .models import Meeting


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


def load_signaler_id():
    return g.user.id


class ParticipateSchema(Schema):
    id = fields.Integer(dump_only=True)
    signaler_id = fields.Integer(load_only=True, missing=load_signaler_id)
    meeting_id = fields.Integer(load_only=True)
    signaler = fields.Nested(UserSchema, dump_only=True)
    meeting = fields.Nested(MeetingSchema, dump_only=True)
    short_opinion = fields.Str()

    @validates("meeting_id")
    def validate_meeting_id(self, value):
        meeting = Meeting.query.filter_by(id=value).first()
        print(meeting.participate_users.filter_by(signaler_id=g.user.id).first() is not None)
        if meeting is None:
            raise ValidationError("meeting id is not exist")
        if meeting.participate_users.filter_by(signaler_id=g.user.id).first() is not None:
            raise ValidationError("user already participated this meeting")
