import binascii
import os

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(40), default=generate_token)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User(username)".format(self.username, self.token)
