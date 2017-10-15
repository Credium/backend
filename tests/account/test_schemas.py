import pytest

from app.account.models import User
from app.account.schemas import UserSchema


class TestUserSchema:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, dict_guest2, publisher1, meeting1):
        self.db = db
        self.guest1 = guest1
        self.dict_guest2 = dict_guest2
        self.publisher1 = publisher1
        self.meeting1 = meeting1

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
        assert user2.id == 4
        assert user2.username == "guest2"

    def test_dump_publisher(self):
        result, data = UserSchema().dump(self.publisher1)
        assert result["username"] == "publisher1"
        assert result["publisher_info"]["make_meetings"][0]["title"] == "title1"
