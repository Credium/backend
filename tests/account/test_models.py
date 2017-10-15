import pytest

from app.account.models import User, generate_token, Follow, PublisherInfo


class TestAccountModel:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1):
        self.guest1 = guest1
        self.publisher1 = publisher1
        self.publisher2 = User(username="publisher2", password="publisher", type="publisher")
        self.publisher2.publisher_info = PublisherInfo(description="the second publisher")

        self.follow1 = Follow(subject=self.guest1)
        self.follow2 = Follow(subject=self.guest1)

        self.publisher1.follower.append(self.follow1)
        self.publisher2.follower.append(self.follow2)
        db.session.add(self.guest1, self.publisher1)
        db.session.add(self.publisher2)
        db.session.commit()

    def test_guest_create(self, db):
        user = User.query.filter_by(username="guest1").first()
        assert user.username == "guest1"

    def test_generate_token(self):
        token = generate_token()
        assert len(token) == 40

    def test_create_publisher_info(self):
        assert self.publisher1.is_publisher
        assert self.publisher1.publisher_info.description == "the first publisher"

    def test_guest_following(self):
        assert self.guest1.following[0].object.username == "publisher1"
        assert self.guest1.following[1].object.username == "publisher2"

    def test_publisher1_follower(self):
        assert self.publisher1.follower[0].subject.username == "guest1"

    def test_delete_guest_publisher1_folower(self, db):
        follow = Follow.query.filter_by(subject=self.guest1,
                                        object=self.publisher1).first()
        db.session.delete(follow)
        assert not Follow.query.filter_by(object=self.publisher1).count()
