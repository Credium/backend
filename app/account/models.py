import binascii
import os

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.choice import ChoiceType
from werkzeug.security import check_password_hash, generate_password_hash

from app.application import db, login_manager


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


class User(UserMixin, db.Model):
    TYPES = [
        ("admin", "admin"),
        ("signaler", "signaler"),
        ("publisher", "publisher")
    ]
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    type = db.Column(ChoiceType(TYPES), default="signaler")
    token = db.Column(db.String(40), default=generate_token, unique=True)
    publisher_info = relationship("PublisherInfo", uselist=False, back_populates="user")

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_superuser(self):
        return self.type == "admin"

    @property
    def is_publisher(self):
        return self.type == "publisher"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def change_token(self):
        self.token = generate_token()
        db.session.add(self)
        db.session.commit()

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
        }
        return "User(username={username}," \
               "password_hash={password_hash}," \
               "token={token})".format(**user_info)


class PublisherInfo(db.Model):
    __tablename__ = "publisher_info"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", uselist=False, back_populates="publisher_info")
    about = db.Column(db.String(), nullable=True)
    accumulate_money = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            self.user.username)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
