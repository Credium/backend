from flask import url_for

from app.account.models import User


class TestAccountView:

    def get_guest1_queryset(self):
        return User.query.filter_by(username="guest1")

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
        assert response.data.decode("utf-8") == "guest1"

    def test_login_fail(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest",
            "password": "guest1"
        }
        response = client.post(url, data=data)
        assert response.status_code == 401
        assert response.data.decode("utf-8") == "invalidate"

    def test_logout(self, client):
        url = url_for("account.logout")
        guest1 = self.get_guest1_queryset().first()
        header = self.get_auth_header(guest1.token)
        response = client.get(url,
                              header=header)
        assert response.status_code == 200

    def test_register(self, client):
        url = url_for("account.register")
        data = {
            "username": "guest2",
            "password": "guest2"
        }
        response = client.post(url, data)
        assert response.status_code == 201
        assert "token" in response.data.decode('utf-8')

    def test_delete(self, client):
        url = url_for("account.delete")
        guest1 = self.get_guest1_queryset()
        client.post(url,
                    header=self.get_auth_header(guest1.first().token))
        assert guest1.first() is None

    def test_update(self, client):
        url = url_for("account.update")
        guest1 = self.get_guest1_queryset().first()
        data = {
            "username": "guest1_update",
            "password": "guest1_update"
        }
        response = client.post(url,
                               data=data,
                               header=self.get_auth_header(guest1.token))
        guest1_update = self.get_guest1_queryset().first()
        assert response.status_code == 200
        assert guest1_update.username == "guest1_update"

    def test_user_info(self, client):
        url = url_for("account.user_info")
        guest1 = self.get_guest1_queryset().first()
        response = client.get(url,
                              header=self.get_auth_header(guest1.token))
        assert response.status_code == 200
        assert response.data.decode("utf-8")["username"] == "guest1"
