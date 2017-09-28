import binascii
import os

from app import db


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(40), default=generate_token)
    authenticated = db.Column(db.Boolean, default=False)

    def verify_password(self, password_hash):
        return self.password_hash == password_hash

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def dict(self):
        info = {
            "id": self.id,
            "username": self.username,
            "token": self.token,
        }
        return info

    def __repr__(self):
        user_info = {
            "username": self.username,
            "password_hash": self.password_hash,
            "token": self.token,
            "authenticated": self.authenticated,
        }
        return "User(username={username},password_hash={password_hash},token={token},authenticated={authenticated})".format(**user_info)
