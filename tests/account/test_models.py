import pytest

from app.account.models import Follow, PublisherInfo, User, generate_token


class TestAccountModel:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1):
        self.db = db
        self.guest1 = guest1
        self.publisher1 = publisher1
        self.publisher2 = User(username="publisher2", password="publisher", type="publisher")
        self.publisher2.publisher_info = PublisherInfo(description="the second publisher")

        self.follow1 = Follow(following=self.guest1)
        self.follow2 = Follow(following=self.guest1)

        self.publisher1.publisher_info._follower.append(self.follow1)
        self.publisher2.publisher_info._follower.append(self.follow2)
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
        assert self.guest1.following[0].user.username == "publisher1"
        assert self.guest1.following[1].user.username == "publisher2"

    def test_publisher1_follower(self):
        assert self.publisher1.publisher_info.follower[0].username == "guest1"

    def test_delete_guest_publisher1_folower(self):
        print(Follow.query.all())
        follow = Follow.query.filter_by(following=self.guest1,
                                        follower=self.publisher1.publisher_info).first()
        self.db.session.delete(follow)
        assert not Follow.query.filter_by(follower=self.publisher1.publisher_info).count()
