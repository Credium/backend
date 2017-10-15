from flask import url_for
import pytest
from app.account.models import User, generate_token


class TestAccountView:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1):
        self.guest1 = guest1
        self.publisher1 = publisher1

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
        # Default Content-type is 'application/x-www-form-urlencoded'
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
        assert response.json["error"] == "username is not matched any User model's row"

    def test_login_fail_invalid_password(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest1",
            "password": "wrong"
        }
        response = client.post(url, data=data)
        assert response.status_code == 401
        print(response.json)
        assert response.json["error"] == "password is not validation"

    def test_login_request_content_type_x_www(self, client):
        url = url_for("account.login")
        data = "username=guest1&password=guest1"
        response = client.post(url, data=data, content_type='application/x-www-form-urlencoded')
        assert response.status_code == 200

    def test_login_request_content_type_x_www_with_json_data(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest1",
            "password": "guest1"
        }
        response = client.post(url, data=data, content_type='application/x-www-form-urlencoded')
        assert response.status_code == 200

    def test_login_request_content_type_form_data_with_json_data(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest1",
            "password": "guest1"
        }
        response = client.post(url, data=data, content_type='multipart/form-data')
        assert response.status_code == 200

    def test_login_request_content_type_text(self, client):
        url = url_for("account.login")
        data = "username=guest1&password=guest1"
        response = client.post(url, data=data, content_type='text/plain')
        assert response.status_code == 400

    def test_login_request_content_type_text_with_json_data(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest1",
            "password": "guest1"
        }
        response = client.post(url, data=data, content_type='text/plain')
        assert response.status_code == 400

    def test_login_request_content_type_json(self, client):
        url = url_for("account.login")
        data = "username=guest1&password=guest1"
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 400

    def test_login_request_content_type_json_with_json_data(self, client):
        url = url_for("account.login")
        data = {
            "username": "guest1",
            "password": "guest1"
        }
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 400

    def test_login_request_content_type_form_data(self, client):
        url = url_for("account.login")
        data = "username=guest1&password=guest1"
        response = client.post(url, data=data, content_type='multipart/form-data')
        assert response.status_code == 400

    def test_logout_success(self, client):
        url = url_for("account.logout")
        token = self.guest1.token
        header = self.get_auth_header(self.guest1.token)
        response = client.get(url,
                              headers=header)
        assert response.status_code == 200
        assert token != self.guest1.token

    def test_logout_fail(self, client):
        url = url_for("account.logout")
        invalid_token = generate_token()
        header = self.get_auth_header(invalid_token)
        response = client.get(url,
                              headers=header)
        assert response.status_code == 401
        assert response.json["status"] == False
        assert response.json["error"] == "token is not valid"

    def test_register_success(self, client, dict_guest2):
        url = url_for("account.register")
        data = dict_guest2
        response = client.post(url, data=data, content_type='multipart/form-data')
        assert response.status_code == 201
        assert "token" in response.json
        assert len(response.json["token"]) == 40

    def test_register_fail_duplicated_username(self, client, dict_guest2):
        url = url_for("account.register")
        data = dict_guest2
        data["username"] = "guest1"
        response = client.post(url, data=data)
        assert response.status_code == 400
        assert response.json["errors"]["username"] == ["username is not unique"]

    def test_delete_success(self, client):
        assert self.get_guest1() is not None
        url = url_for("account.delete")
        response = client.delete(url,
                                 headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 200
        assert self.get_guest1() is None

    def test_delete_fail(self, client):
        assert self.get_guest1() is not None
        url = url_for("account.delete")
        invalid_token = generate_token()
        response = client.delete(url,
                                 headers=self.get_auth_header(invalid_token))
        assert response.status_code == 401
        assert response.json["status"] == False
        assert response.json["error"] == "token is not valid"
        assert self.get_guest1() is not None

    def test_update_success(self, client):
        url = url_for("account.update")
        data = {
            "username": "guest1_update",
            "password": "guest1_update"
        }
        response = client.put(url,
                              data=data,
                              headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 200
        assert self.guest1.username == "guest1_update"

    def test_update_fail(self, client):
        url = url_for("account.update")
        data = {
            "username": "guest1_update",
            "password": "guest1_update"
        }
        response = client.put(url,
                              data=data,
                              headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 200
        assert response.json["status"] == True
        assert self.guest1.username == "guest1_update"

    def test_user_info(self, client):
        url = url_for("account.user_info")
        response = client.get(url,
                              headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 200
        assert response.json["username"] == "guest1"

    def test_recommend_publisher(self, client):
        url = url_for("account.recommend_publisher")
        response1 = client.get(url)
        assert response1.status_code == 200
