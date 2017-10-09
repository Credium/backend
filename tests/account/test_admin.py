from flask import url_for


class TestAdminView:

    def test_admin_index_page(self, client):
        url = url_for("admin.index")
        response = client.get(url)
        page_source = response.data.decode()

        assert "<h1>Login</h1>" in page_source
        assert '<input type="text" name="username" />' in page_source
        assert '<input type="password" name="password" />' in page_source
        assert '<button type="submit" >Submit</button>' in page_source

    def test_admin_login_success(self, client):
        url = url_for("admin.login")
        data = {
            "username": "admin",
            "password": "admin"
        }
        response = client.post(url, data=data, follow_redirects=True)
        page_source = response.data.decode()

        assert "<h1>환영합니다. admin님</h1>" in page_source
        assert '<input type="text" name="username" />' not in page_source
        assert '<input type="password" name="password" />' not in page_source

    def test_admin_login_fail(self, client):
        url = url_for("admin.login")
        data = {
            "username": "guest",
            "password": "guest"
        }
        response = client.post(url, data=data, follow_redirects=True)
        page_source = response.data.decode()

        assert "<h1>Login</h1>" in page_source
        assert '<input type="text" name="username" />' in page_source
        assert '<input type="password" name="password" />' in page_source
        assert '<button type="submit" >Submit</button>' in page_source

    def test_admin_logout(self, client):
        url = url_for("admin.login")
        data = {
            "username": "admin",
            "password": "admin"
        }
        response = client.post(url, data=data, follow_redirects=True)
        page_source = response.data.decode()

        assert "<h1>환영합니다. admin님</h1>" in page_source
        url = url_for("admin.logout")
        response = client.post(url, data=data, follow_redirects=True)
        page_source = response.data.decode()

        assert "<h1>Login</h1>" in page_source
        assert '<input type="text" name="username" />' in page_source
        assert '<input type="password" name="password" />' in page_source
        assert '<button type="submit" >Submit</button>' in page_source
