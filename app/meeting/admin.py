from app.application import admin, db
from app.views import ModelView

from .models import Meeting, Participate

admin.add_view(ModelView(Meeting, db.session, endpoint="meetings"))
admin.add_view(ModelView(Participate, db.session))
