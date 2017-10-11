from sqlalchemy.orm import relationship

from app.application import db


class PersonDemand(db.Model):
    __tablename__ = "person_demand"
    id = db.Column(db.Integer,
                   primary_key=True)
    full_name = db.Column(db.String)
    description = db.Column(db.String)
    profile_photo_path = db.Column(db.String)
    job = db.Column(db.String(150))
    reference_link = db.Column(db.String)
    is_checked_by_admin = db.Column(db.Boolean,
                                    default=False)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            self.full_name)


class MeetingDemand(db.Model):
    __tablename__ = "meeting_demand"
    id = db.Column(db.Integer,
                   primary_key=True)
    signaler_id = db.Column(db.Integer,
                            db.ForeignKey("users.id"))
    publisher_id = db.Column(db.Integer,
                             db.ForeignKey("publisher_info.id"))
    signaler = relationship("User",
                            backref="demanding_meetings")
    publisher = relationship("PublisherInfo",
                             backref="demanded_meetings")
    title = db.Column(db.String)
    introduce = db.Column(db.String)
    is_enabled = db.Column(db.Boolean,
                           default=False)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            self.title)
