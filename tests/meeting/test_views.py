import pytest
from flask import url_for
from app.demand.models import MeetingDemand


class TestMeetingDemandView:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1):
        self.guest1 = guest1
        self.publisher1 = publisher1

    def get_auth_header(self, token):
        return {
            "Authorization": token
        }

    def test_success_meeting_demand_create(self, client):
        url = url_for('demand.demand_meeting_create', publisher_pk=self.publisher1.id)
        data = {
            "title": "바둑 배우고 싶어요",
            "introduce": "바둑 1년 째 실력이 전혀 안늘어요ㅠ 도와주세여. 고수님"
        }
        response = client.post(url,
                               data,
                               header=self.get_auth_header(self.guest1.token))
        assert response.status_code == 201
