import pytest

from app.account.models import User
from app.account.schemas import UserSchema


class TestUserSchema:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, dict_guest2):
        self.db = db
        self.guest1 = guest1
        self.dict_guest2 = dict_guest2

    def test_read_guest1(self):
        schema = UserSchema()
        result = schema.dump(self.guest1)
        assert result.data["username"] == "guest1"
        assert result.data["type"] == "signaler"

    def test_load_guest2(self):
        schema = UserSchema()
        clean_data = schema.load(self.dict_guest2)
        user2 = User(**clean_data.data)
        self.db.session.add(user2)
        self.db.session.commit()
        assert user2.id == 3
        assert user2.username == "guest2"
