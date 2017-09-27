import pytest
from app.account.models import User


@pytest.fixture(autouse=True)
def create_guest1(db):
    user = User(username="guest1", password="guest1")
    db.session.add(user)
    db.session.commit()
    return user