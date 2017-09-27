import pytest
from flask import url_for

from app import create_app, db
from app.account.models import User


@pytest.fixture(scope="session")
def app():
    app = create_app('testing')
    app.test_request_context().push()
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


@pytest.fixture(scope="session")
def create_guest1():
    user = User(username="guest1", password="guest1")
    db.session.add(user)
    db.session.commit()
    return user


def test_setup(app, create_guest1):
    pass


def test_guest_add(app):
        user = User.query.filter_by(username="guest1").first()
        assert user.username == "guest1"


def test_login_success_api(client):
        user = User.query.filter_by(username="guest1").first()
        assert user.username == "guest1"

        data = {
            "username": "guest1",
            "password": "guest1"
        }
        url = url_for('account.login')
        response = client.post(url, data=data)
        assert response.data.decode('utf-8') == 'guest1'


def test_login_fail_api(client):
        data = {
            "username": "gue",
            "password": "password"
        }
        url = url_for('account.login')
        response = client.post(url, data=data)
        assert response.data.decode('utf-8') == 'invalidate'
