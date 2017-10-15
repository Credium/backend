import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app.account.models import User
from app.application import db


class Meeting(db.Model):
    __tablename__ = "meetings"
    id = db.Column(db.Integer,
                   primary_key=True)
    publisher_id = db.Column(db.Integer,
                             db.ForeignKey("publisher_info.id"))
    publisher = relationship("PublisherInfo",
                             backref="make_meetings")
    title = db.Column(db.String)
    content = db.Column(db.String)
    maximum_people = db.Column(db.Integer)
    location = db.Column(db.String(32))
    entry_fee = db.Column(db.Integer)
    entry_fee_type = db.Column(db.String(16))

    entry_due_time = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime,
                             default=datetime.datetime.utcnow)
    participate_users = db.relationship("Participate",
                                        back_populates="meeting",
                                        lazy="dynamic")

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            self.title)


class Participate(db.Model):
    __tablename__ = "participate"
    id = db.Column(db.Integer,
                   primary_key=True)
    signaler_id = db.Column(db.Integer,
                            db.ForeignKey("users.id"))
    meeting_id = db.Column(db.Integer,
                           db.ForeignKey("meetings.id"))
    signaler = relationship("User",
                            backref="participate_meetings")
    meeting = relationship("Meeting",
                           back_populates="participate_users")
    short_opinion = db.Column(db.String(100))

    def __repr__(self):
        return "<%s %s->%s>" % (self.__class__.__name__,
                                self.signaler.username,
                                self.meeting.title)


Meeting.members = association_proxy("participate_users", "signaler")
User.meetings = association_proxy("participate_meetings", "meeting")
