import pytest
from flask import url_for

from app.meeting.models import Meeting


class TestMeetingView:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1, follow1):
        self.db = db
        self.guest1 = guest1
        self.publisher1 = publisher1
        self.pub1_info = self.publisher1.publisher_info
        for i in range(10):
            meeting = Meeting(title="title{}".format(i))
            self.db.session.add(meeting)
            self.db.session.commit()

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
        assert response.json["title"] == dict_meeting1["title"]
        assert dict_meeting1["title"] in response.json["meeting_photo_path"]

        created_meeting = Meeting.query.filter_by(publisher=self.pub1_info).first()
        assert self.pub1_info.make_meetings[0] == created_meeting


    def test_get_publisher_meeting_success(self, client, dict_meeting1):
        self.test_meeting_create_success(client, dict_meeting1)
        url = url_for("meeting.publisher_meeting_list",
                      publisher_id=self.publisher1.id)
        response = client.get(url)
        assert response.status_code == 200
        assert response.json[0]["title"] == dict_meeting1["title"]
        assert dict_meeting1["title"] in response.json[0]["meeting_photo_path"]

    def test_meeting_list_success(self, client):
        url = url_for("meeting.meeting_list")
        response = client.get(url,
                              headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 200
        assert response.json[0]["title"] == "title9"

    def test_meeting_list_pagination(self, client):
        base_url = url_for("meeting.meeting_list")

        url = base_url + "?count=5"
        response = client.get(url,
                              headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 200
        assert len(response.json) == 5

        max_id = int(response.json[-1]["id"])
        url = base_url + "?max_id={}".format(max_id)
        response = client.get(url,
                              headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 200
        assert len(response.json) == 5
        assert response.json[0]["id"] == max_id - 1
