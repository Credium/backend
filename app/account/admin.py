from app.application import admin, db
from app.views import ModelView

from .models import Follow, PublisherInfo, User

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(PublisherInfo, db.session))
admin.add_view(ModelView(Follow, db.session))
