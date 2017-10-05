import pytest

from app import db as _db
from app import create_app
from app.account.models import User


@pytest.yield_fixture(scope="session")
def app():
    app = create_app('testing')
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.yield_fixture(scope="function")
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture(autouse=True)
def admin_user(db):
    admin_user = User(username="admin", password="admin", is_superuser=True)
    db.session.add(admin_user)
    db.session.commit()
    return admin_user
