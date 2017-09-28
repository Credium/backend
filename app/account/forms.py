from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length

from .models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(4, 64)])
    password = PasswordField('Password', validators=[DataRequired()])

    def auth(self):
        username = self.username.data
        password_hash = self.password.data
        user = User.query.filter_by(username=username).first()
        if user is None:
            return None
        if not user.verify_password(password_hash):
            return None

        return user
