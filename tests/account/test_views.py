import pytest
from flask import url_for

from app.account.models import User


class TestAccountView:

    def get_guest1(self):
        return User.query.filter_by(username="guest1").first()

    def get_auth_header(self, token):
        return {
            "Authorization": token
        }

    def test_login_success(self, client):
        url = url_for('account.login')
        data = {
            "username": "guest1",
            "password": "guest1"
        }
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert response.json["ok"] == True
        assert response.json["user"]["username"] == "guest1"

    def test_login_fail_invalid_form(self, client):
        url = url_for("account.login")
        data = {
            "username": "as",
            "password": "guest1"
        }
        response = client.post(url, data=data)
        assert response.status_code == 405
        assert response.json["ok"] == False
        assert response.json["error"] == "invalidated form"

    def test_login_fail_invalid_user(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest",
            "password": "guest1"
        }
        response = client.post(url, data=data)
        assert response.status_code == 405
        assert response.json["ok"] == False
        assert response.json["error"] == "invalidated user"

    @pytest.mark.skip()
    def test_logout(self, client, guest1):
        url = url_for("account.logout")
        header = self.get_auth_header(guest1.token)
        response = client.get(url,
                              header=header)
        assert response.status_code == 200

    @pytest.mark.skip()
    def test_register(self, client):
        url = url_for("account.register")
        data = {
            "username": "guest2",
            "password": "guest2"
        }
        response = client.post(url, data)
        assert response.status_code == 201
        assert "token" in response.data.decode('utf-8')

    @pytest.mark.skip()
    def test_delete(self, client, guest1):
        url = url_for("account.delete")
        client.post(url,
                    header=self.get_auth_header(guest1.token))
        assert self.get_guest1() is None

    @pytest.mark.skip()
    def test_update(self, client, guest1):
        url = url_for("account.update")
        data = {
            "username": "guest1_update",
            "password": "guest1_update"
        }
        response = client.post(url,
                               data=data,
                               header=self.get_auth_header(guest1.token))
        assert response.status_code == 200
        assert guest1.username == "guest1_update"

    @pytest.mark.skip()
    def test_user_info(self, client, guest1):
        url = url_for("account.user_info")
        response = client.get(url,
                              header=self.get_auth_header(guest1.token))
        assert response.status_code == 200
        assert response.data.decode("utf-8")["username"] == "guest1"
