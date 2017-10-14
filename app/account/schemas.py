import os

from marshmallow import Schema, ValidationError, fields, validates

from .models import User


class LoginSchema(Schema):
    username = fields.String()
    password = fields.String()

    @validates('username')
    def validate_username(self, value):
        pass

    @validates('password')
    def validate_password(self, value):
        pass

    def _do_load(self, *args, **kwargs):
        result, errors = super(LoginSchema, self)._do_load(*args, **kwargs)
        data, _ = args

        user, error_msg = self.get_valid_user(data["username"], data["password"])
        if error_msg:
            errors["error"] = error_msg
        if user is not None:
            result["user"] = UserSchema().dump(user)

        return result, errors

    def get_valid_user(self, username, password):
        error_msg = ""
        user = User.query.filter_by(username=username).first()
        if user is None:
            error_msg = "username is not matched any User model's row"
            return None, error_msg
        if not user.verify_password(password):
            error_msg = "password is not validation"
            return None, error_msg
        return user, error_msg


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

    @validates("username")
    def validate_username(self, value):
        user = User.query.filter_by(username=value).first()
        if user is not None:
            raise ValidationError("username is not unique")

    @validates('profile_photo_path')
    def validate_profile_photo_path(self, image):
        if not isinstance(image, str):
            raise ValidationError("profile_photo_path must be a str")
        if not os.path.isfile(image):
            raise ValidationError("profile photo path value is not image")

    def get_type(self, obj):
        if isinstance(obj.type, str):
            return obj.type
        return obj.type.value