from sqlalchemy.orm import relationship

from app.application import db


class PersonDemand(db.Model):
    __tablename__ = "person_demand"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    explain = db.Column(db.String)
    job = db.Column(db.String(150))
    reference_link = db.Column(db.String)
    # todo profile field

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            self.name)


class MeetingDemand(db.Model):
    __tablename__ = "meeting_demand"
    id = db.Column(db.Integer, primary_key=True)
    signaler_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher_info.id"))
    signaler = relationship("User", back_populates="demanding_meetings")
    publisher = relationship("PublisherInfo", back_populates="demanded_meetings")
    title = db.Column(db.String)
    introduce = db.Column(db.String)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__,
                            self.title)
