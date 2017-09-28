from app.account.models import User


class TestAccountModel:

    def test_guest_create(self, db):
        user = User.query.filter_by(username="guest1").first()
        assert user.username == "guest1"
