import datetime

import pytest

from app.account.models import PublisherInfo, User
from app.meeting.models import Meeting


@pytest.fixture
def guest1(db):
    user = User(username="guest1", password="guest1")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def publisher1(db):
    user = User(username="publisher1", password="publisher", type="publisher")
    user.publisher_info = PublisherInfo(about="the first publisher")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def meeting1(db, publisher1):
    meeting_time = datetime.datetime.strptime("2014-01-21 00:00:00", "%Y-%m-%d %H:%M:%S")
    meeting = Meeting(publisher=publisher1.publisher_info,
                       title="title1",
                       content="content1",
                       meeting_time=meeting_time,
                       participation_number="5",
                       acceptance_number="10"
                       )
    db.session.add(meeting)
    db.session.commit()
    return meeting
