import pytest
from flask import url_for

from app import create_app


@pytest.fixture
def app():
    app = create_app('testing')
    app.test_request_context().push()
    return app


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


def test_login_success_api(app, client):
    data = {
        "username": "guest1",
        "password": "guest1"
    }
    url = url_for('account.login')
    response = client.post(url, data=data)
    assert response.data.decode('utf-8') == 'validate'


def test_login_fail_api(app, client):
    data = {
        "username": "gue",
        "password": "password"
    }
    url = url_for('account.login')
    response = client.post(url, data=data)
    assert response.data.decode('utf-8') == 'invalidate'
