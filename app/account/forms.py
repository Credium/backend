from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Length, DataRequired
from .models import User
from flask import abort


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(4, 64)])
    password = PasswordField('Password', validators=[DataRequired()])

    def auth(self):
        username = self.username.data
        password = self.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if user.verify_password(password):
                return user
        abort(404)
