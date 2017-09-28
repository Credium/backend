from flask import url_for


class TestAccountView:

    def test_login_success(self, client):
        url = url_for('account.login')
        data = {
            "username": "guest1",
            "password": "guest1"
        }
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'guest1'

    def test_login_fail(self, client):
        url = url_for('account.login')
        data = {
            "username": "guest",
            "password": "guest1"
        }
        response = client.post(url, data=data)
        assert response.status_code == 401
        assert response.data.decode('utf-8') == 'invalidate'
