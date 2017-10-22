import os

from flask import current_app, g
from marshmallow import Schema, ValidationError, fields, validates, validates_schema, post_load

from .models import User


class LoginSchema(Schema):
    username = fields.String()
    password = fields.String()

    @validates_schema
    def validate_login(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise ValidationError("username is not matched any User model's row", "username")
        if not user.verify_password(password):
            raise ValidationError("password is not validation", "password")
        self.user = user

    @post_load
    def user_schema_wrap(self, item):
        schema = UserSchema().dump(self.user)
        return schema.data


class PublisherInfoSchema(Schema):
    description = fields.Str()
    is_registered = fields.Bool()
    make_meetings = fields.Nested("app.meeting.schemas.MeetingSchema",
                                  many=True,
                                  dump_only=True)
    signaler_numbers = fields.Integer(dump_only=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    password = fields.String(load_only=True)
    type = fields.Method("get_type")
    token = fields.String(dump_only=True)
    full_name = fields.String()
    profile_photo_path = fields.String()
    job = fields.String()
    phone_number = fields.String()
    publisher_info = fields.Nested(PublisherInfoSchema)
    balance = fields.Integer(dump_only=True)

    @validates("username")
    def validate_username(self, value):
        user = User.query.filter_by(username=value).first()
        if user is not None:
            raise ValidationError("username is not unique")

    @validates('profile_photo_path')
    def validate_profile_photo_path(self, image):
        if not isinstance(image, str):
            raise ValidationError("profile_photo_path must be a str")
        path = os.path.join(current_app.config["MEDIA_FILE_PATH"], image)
        if not os.path.isfile(path):
            raise ValidationError("profile photo path value is not image")

    def get_type(self, obj):
        if isinstance(obj.type, str):
            return obj.type
        return obj.type.value


class PublisherInfoToUserSchema(Schema):
    id = fields.Integer(attribute="user.id")
    username = fields.String(attribute="user.username")
    type = fields.Method("get_type", attribute="user.type")
    token = fields.String(attribute="user.token")
    full_name = fields.String(attribute="user.full_name")
    profile_photo_path = fields.String(attribute="user.profile_photo_path")
    job = fields.String(attribute="user.job")
    phone_number = fields.String(attribute="user.publisher_info")
    publisher_info = fields.Nested(PublisherInfoSchema, attribute="user.publisher_info")

    def get_type(self, obj):
        if isinstance(obj.type, str):
            return obj.type
        return obj.type.value


def load_following_id():
    return g.user.id


class FollowSchema(Schema):
    following_id = fields.Integer(load_only=True, missing=load_following_id)
    follower_id = fields.Method(load_only=True, deserialize="load_follower_id")
    following = fields.Nested(UserSchema, dump_only=True)
    follower = fields.Nested(UserSchema, dump_only=True)

    @validates("follower_id")
    def validate_follower_id(self, value):
        if value is None:
            raise ValidationError("publisher id is not exist or publisher")

    def load_follower_id(self, value):
        publisher = User.query.filter_by(id=value).first()
        if publisher is not None and publisher.is_publisher:
            return publisher.publisher_info.id
        else:
            return None
