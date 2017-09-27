from app.account.models import User


def test_guest_create(db):
    user = User.query.filter_by(username="guest1").first()
    assert user.username == "guest1"
