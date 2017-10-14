import pytest
from flask import url_for
from app.meeting.models import Meeting


class TestMeetingView:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1):
        self.guest1 = guest1
        self.publisher1 = publisher1
        self.pub1_info = self.publisher1.publisher_info

    def get_auth_header(self, token):
        return {
            "Authorization": token
        }

    def test_meeting_create_success(self, client, dict_meeting1):
        url = url_for("meeting.meeting_create")
        data = dict_meeting1
        response = client.post(url,
                               data=data,
                               headers=self.get_auth_header(self.publisher1.token))
        assert response.status_code == 201
        assert response.json["title"] == "바둑 가르쳐 드립니다"

        created_meeting = Meeting.query.filter_by(publisher=self.pub1_info).first()
        assert created_meeting.id == 1
        assert self.pub1_info.make_meetings[0] == created_meeting
