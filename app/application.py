from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_admin import Admin
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(base_template="admin/index.html")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from .views import AdminIndexView
    admin.init_app(app, index_view=AdminIndexView())

    from .blueprints import all_blueprints
    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)

    return app
