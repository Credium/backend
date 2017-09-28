import pytest

from app import db as _db
from app import create_app


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
