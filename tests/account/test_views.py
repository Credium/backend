from flask import url_for
from PIL import Image

from app.account.models import User, generate_token


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
        assert response.json["username"] == "guest1"
        assert response.json["full_name"] == "김의사"

    def test_login_fail_invalid_user(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest",
            "password": "guest1"
        }
        response = client.post(url, data=data)
        assert response.status_code == 401
        print(response.json)
        assert response.json["username"] == ["username is not matched any User model's row"]

    def test_logout_success(self, client, guest1):
        url = url_for("account.logout")
        token = guest1.token
        header = self.get_auth_header(guest1.token)
        response = client.get(url,
                              headers=header)
        assert response.status_code == 200
        assert token != guest1.token

    def test_logout_fail(self, client, guest1):
        url = url_for("account.logout")
        invalid_token = generate_token()
        header = self.get_auth_header(invalid_token)
        response = client.get(url,
                              headers=header)
        assert response.status_code == 401
        assert response.json["status"] == False
        assert response.json["error"] == "token is not valid"

    def test_register_success(self, client):
        url = url_for("account.register")
        image = Image.new('RGB', (100, 100))
        data = dict(username="guest3",
                    password="guest1",
                    type="signaler",
                    profile_photo=image,
                    job="의사선생님",
                    phone_number="01099725801",
                    full_name="김의사"
                    )
        response = client.post(url, data=data, content_type='multipart/form-data')
        assert response.status_code == 201
        print(response.json)
        assert "token" in response.json
        assert len(response.json["token"]) == 40

    def test_register_fail(self, client):
        url = url_for("account.register")
        image = Image.new('RGB', (100, 100))
        data = dict(username="guest1",
                    password="guest1",
                    type="signaler",
                    profile_photo=image,
                    job="의사선생님",
                    phone_number="01099725801",
                    full_name="김의사"
                    )
        response = client.post(url, data=data)
        assert response.status_code == 400
        assert response.json["errors"]["username"] == ["username is not unique"]

    def test_delete_success(self, client, guest1):
        assert self.get_guest1() is not None
        url = url_for("account.delete")
        response = client.delete(url,
                                 headers=self.get_auth_header(guest1.token))
        assert response.status_code == 200
        assert self.get_guest1() is None

    def test_delete_fail(self, client, guest1):
        assert self.get_guest1() is not None
        url = url_for("account.delete")
        invalid_token = generate_token()
        response = client.delete(url,
                                 headers=self.get_auth_header(invalid_token))
        assert response.status_code == 401
        assert response.json["status"] == False
        assert response.json["error"] == "token is not valid"
        assert self.get_guest1() is not None

    def test_update_success(self, client, guest1):
        url = url_for("account.update")
        data = {
            "username": "guest1_update",
            "password": "guest1_update"
        }
        response = client.put(url,
                              data=data,
                              headers=self.get_auth_header(guest1.token))
        assert response.status_code == 200
        assert guest1.username == "guest1_update"

    def test_update_fail(self, client, guest1):
        url = url_for("account.update")
        data = {
            "username": "guest1_update",
            "password": "guest1_update"
        }
        response = client.put(url,
                              data=data,
                              headers=self.get_auth_header(guest1.token))
        assert response.status_code == 200
        assert response.json["status"] == True
        assert guest1.username == "guest1_update"

    def test_user_info(self, client, guest1):
        url = url_for("account.user_info")
        response = client.get(url,
                              headers=self.get_auth_header(guest1.token))
        assert response.status_code == 200
        assert response.json["username"] == "guest1"
