from app.application import db
from app.views import ModelView

from app.account.models import User, PublisherInfo, Follow
from app.demand.models import MeetingDemand, PersonDemand
from app.meeting.models import AbcMeeting, Participate


def add_views_to_admin(admin):
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(PublisherInfo, db.session))
    admin.add_view(ModelView(Follow, db.session))
    admin.add_view(ModelView(MeetingDemand, db.session))
    admin.add_view(ModelView(PersonDemand, db.session))
    admin.add_view(ModelView(AbcMeeting, db.session))
    admin.add_view(ModelView(Participate, db.session))
