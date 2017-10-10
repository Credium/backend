from app.application import admin, db
from app.views import ModelView

from .models import MeetingDemand, PersonDemand

admin.add_view(ModelView(MeetingDemand, db.session))
admin.add_view(ModelView(PersonDemand, db.session))
