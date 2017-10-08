import datetime

from sqlalchemy.orm import relationship

from app.application import db


class Meeting(db.Model):
    __tablename__ = "meeting"
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher_info.id"))
    publisher = relationship("PublisherInfo",
                             back_populates="make_meetings")
    title = db.Column(db.String)
    content = db.Column(db.String)
    meeting_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    participation_number = db.Column(db.Integer)
    acceptance_number = db.Column(db.Integer)
    participate_users = db.relationship("Participate", back_populates="meeting")

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            self.title)


class Participate(db.Model):
    __tablename__ = "participate"
    id = db.Column(db.Integer, primary_key=True)
    signaler_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    meeting_id = db.Column(db.Integer, db.ForeignKey("meeting.id"))
    signaler = relationship("User", back_populates="participate_meetings")
    meeting = relationship("Meeting", back_populates="participate_users")

    def __repr__(self):
        return "<%s %s->%s>" % (self.__class__.__name__,
                                self.signaler.username,
                                self.meeting.title)
