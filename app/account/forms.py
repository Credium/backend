from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(4, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
