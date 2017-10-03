from app import admin, db
from app.views import ModelView

from .models import User

admin.add_view(ModelView(User, db.session))
