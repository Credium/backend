import pytest

from app.account.models import Follow, PublisherInfo, User


class TestPublisherModel:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db):
        self.guest = User(username="guest", password="guest")

        self.publisher1 = User(username="publisher1", password="publisher", type="publisher")
        self.publisher1.publisher_info = PublisherInfo(description="the first publisher")

        self.publisher2 = User(username="publisher2", password="publisher", type="publisher")
        self.publisher2.publisher_info = PublisherInfo(description="the second publisher")

        self.follow1 = Follow(subject=self.guest)
        self.follow2 = Follow(subject=self.guest)

        self.publisher1.follower.append(self.follow1)
        self.publisher2.follower.append(self.follow2)
        db.session.add(self.guest, self.publisher1)
        db.session.add(self.publisher2)
        db.session.commit()

    def test_create_publisher_info(self):
        assert self.publisher1.is_publisher
        assert self.publisher1.publisher_info.description == "the first publisher"

    def test_guest_following(self):
        assert self.guest.following[0].object.username == "publisher1"
        assert self.guest.following[1].object.username == "publisher2"

    def test_publisher1_follower(self):
        assert self.publisher1.follower[0].subject.username == "guest"

    def test_delete_guest_publisher1_folower(self, db):
        follow = Follow.query.filter_by(subject=self.guest,
                                        object=self.publisher1).first()
        db.session.delete(follow)
        assert not Follow.query.filter_by(object=self.publisher1).count()
