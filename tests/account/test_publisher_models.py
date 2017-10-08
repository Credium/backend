from app.account.models import User, PublisherInfo
import pytest


class TestPublisherModel:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db):
        self.guest =User(username="guest", password="guest")
        self.publisher = User(username="publisher", password="publisher", type="publisher")
        self.publisher.publisher_info = PublisherInfo(about="the first publisher")
        db.session.add(self.guest, self.publisher)
        db.session.commit()

    def test_create_publisher_info(self):
        assert self.publisher.is_publisher
        assert self.publisher.publisher_info.about == "the first publisher"
