import pytest
from flask import url_for

from app import create_app
from app.account.forms import LoginForm


@pytest.fixture
def app():
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    return app

@pytest.fixture
def client(app):
    client = app.test_client()
    return client

def test_login_success_api(app, client):
    with app.test_request_context():
        data = {
            "username": "guest1",
            "password": "guest1"
        }
        url = url_for('account.login')
        response = client.post(url, data=data)
        assert response.data.decode('utf-8') == 'validate'


def test_login_fail_api(app, client):
    with app.test_request_context():
        data = {
            "username": "gue",
            "password": "password"
        }
        url = url_for('account.login')
        response = client.post(url, data=data)
        assert response.data.decode('utf-8') == 'Hi'
