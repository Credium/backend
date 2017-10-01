import pytest

from app.account.models import User


@pytest.fixture(autouse=True)
def guest1(db):
    user = User(username="guest1", password_hash="guest1")
    db.session.add(user)
    db.session.commit()
    return user
