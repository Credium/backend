import pytest

from app.meeting.models import Meeting


class TestMeetingModel:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1, meeting1, participate1):
        self.guest1 = guest1
        self.publisher1 = publisher1
        self.meeting1 = meeting1
        self.participate1 = participate1

    def test_make_meetings(self):
        make_meeting_count1 = len(self.publisher1.publisher_info.make_meetings)
        make_meeting_count2 = Meeting.query.filter_by(
            publisher=self.publisher1.publisher_info
        ).count()
        assert make_meeting_count1 == make_meeting_count2

    def test_participated_meeting(self):
        participate = self.guest1.participate_meetings[0]
        assert participate.meeting is self.meeting1