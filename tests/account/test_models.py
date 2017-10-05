from app.account.models import User, generate_token


class TestAccountModel:

    def test_guest_create(self, db):
        user = User.query.filter_by(username="guest1").first()
        assert user.username == "guest1"

    def test_generate_token(self):
        token = generate_token()
        assert len(token) == 40
