import pytest
from flask import url_for


class TestParticipateView:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, guest1, publisher1, meeting1):
        self.guest1 = guest1
        self.publisher1 = publisher1
        self.meeting1 = meeting1


    def get_auth_header(self, token):
        return {
            "Authorization": token
        }

    def test_participate_create(self, client):
        url = url_for("meeting.participate_create")
        data = {
            "meeting_id": self.meeting1.id,
            "short_opinion": "ㅎㅇㅎㅇ"
        }
        response1 = client.post(url,
                               data=data,
                               headers=self.get_auth_header(self.guest1.token))
        assert response1.status_code == 201

        response2 = client.post(url,
                               data=data,
                               headers=self.get_auth_header(self.guest1.token))
        assert response2.status_code == 400

    def test_participate_meeting(self, client):
        self.test_participate_create(client)
        url = url_for("meeting.participate_list")
        response1 = client.get(url,
                               headers=self.get_auth_header(self.guest1.token))
        assert response1.status_code == 200
        assert response1.json[0]["title"] == "title1"
