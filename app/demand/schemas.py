import os

from flask import current_app, g
from marshmallow import Schema, ValidationError, fields, validates

from app.account.schemas import UserSchema
from app.helpers import PublisherIDSchemaMixin


class MeetingDemandSchema(Schema, PublisherIDSchemaMixin):
    id = fields.Integer(dump_only=True)
    signaler = fields.Nested(UserSchema, dump_only=True)
    publisher = fields.Nested(UserSchema, dump_only=True)
    title = fields.Str(required=True)
    introduce = fields.Str(required=True)
    is_enabled = fields.Boolean(dump_only=True)


class PersonDemandSchema(Schema):
    full_name = fields.Str()
    description = fields.Str()
    profile_photo_path = fields.Str()
    reference_link = fields.Str()
    job = fields.Str()

    @validates('profile_photo_path')
    def validate_profile_photo_path(self, image):
        if not isinstance(image, str):
            raise ValidationError("profile_photo_path must be a str")
        path = os.path.join(current_app.config["MEDIA_FILE_PATH"], image)
        if not os.path.isfile(path):
            raise ValidationError("profile photo path value is not image")
