import datetime
import os

import pytest
from PIL import Image

from app.account.models import PublisherInfo, User
from app.application import db as _db
from app.application import create_app
from app.meeting.models import Meeting, Participate


@pytest.yield_fixture(scope="session")
def app():
    app = create_app('testing')
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.yield_fixture(scope="function")
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture(autouse=True)
def admin_user(app, db):
    image = Image.new('RGB', (100, 100))
    save_path = os.path.join(app.config["MEDIA_FILE_PATH"], "user_profile", "image03.jpg")
    image.save(save_path)
    admin_user = User(username="admin",
                      password="admin",
                      type="admin",
                      profile_photo_path=os.path.join("user_profile", "image03.jpg"),
                      job="의사선생님",
                      phone_number="01099725801",
                      full_name="김의사"
                      )
    db.session.add(admin_user)
    db.session.commit()
    yield admin_user
    os.remove(save_path)


@pytest.fixture(autouse=True)
def guest1(app, db):
    image = Image.new('RGB', (100, 100))
    save_path = os.path.join(app.config["MEDIA_FILE_PATH"], "user_profile", "image01.jpg")
    image.save(save_path)
    user = User(username="guest1",
                password="guest1",
                type="signaler",
                profile_photo_path=os.path.join("user_profile", "image01.jpg"),
                job="의사선생님",
                phone_number="01099725801",
                full_name="김의사"
                )
    db.session.add(user)
    db.session.commit()
    yield user
    os.remove(save_path)


@pytest.fixture(autouse=True)
def dict_guest2(app, db):
    dict_user = dict(username="guest2",
                     password="guest2",
                     type="signaler",
                     job="의사선생님",
                     phone_number="01099725801",
                     full_name="김의사"
                     )
    return dict_user


@pytest.fixture
def publisher1(db):
    user = User(username="publisher1",
                password="publisher",
                type="publisher",
                full_name="publisher1")
    user.publisher_info = PublisherInfo(description="the first publisher")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def dict_meeting1():
    entry_due_time = datetime.datetime(2012, 3, 3, 10, 10, 10)
    start_time = datetime.datetime(2012, 3, 4, 10, 10, 10)
    end_time = datetime.datetime(2012, 3, 5, 10, 10, 10)
    dict_meeting = dict(
        title="바둑 가르쳐 드립니다",
        content="저 바둑 고수입니다. 저한테서 배우고 싶으신 분들 10명만 오세요.",
        location="서울시",
        entry_fee=200000,
        entry_fee_type="기타",
        entry_due_time=entry_due_time,
        start_time=start_time,
        end_time=end_time,
        maximum_people=10
    )
    return dict_meeting


@pytest.fixture
def meeting1(db, publisher1):
    start_time = datetime.datetime(2012, 3, 3, 10, 10, 10)
    entry_due_time = datetime.datetime(2012, 3, 4, 10, 10, 10)
    end_time = datetime.datetime(2012, 3, 5, 10, 10, 10)
    meeting = Meeting(publisher=publisher1.publisher_info,
                      title="title1",
                      content="content1",
                      location="서울시",
                      entry_fee=200000,
                      entry_fee_type="기타",
                      entry_due_time=entry_due_time,
                      start_time=start_time,
                      end_time=end_time,
                      maximum_people=10
                      )
    db.session.add(meeting)
    db.session.commit()
    return meeting


@pytest.fixture
def participate1(db, guest1, meeting1):
    participate = Participate(signaler=guest1,
                              meeting=meeting1)
    db.session.add(participate)
    db.session.commit()
    return participate
