import copy

import pytest
from flask import url_for


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
        url = url_for('demand.meeting_create')
        data = {
            "publisher_id": self.publisher1.id,
            "title": "바둑 배우고 싶어요",
            "introduce": "바둑 1년 째 실력이 전혀 안늘어요ㅠ 도와주세여. 고수님"
        }
        response = client.post(url,
                               data=data,
                               headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 201

    def test_fail_meeting_demand_create(self, client):
        url = url_for('demand.meeting_create')
        data1 = {
            "publisher_id": self.guest1.id,
            "title": "바둑 배우고 싶어요",
            "introduce": "바둑 1년 째 실력이 전혀 안늘어요ㅠ 도와주세여. 고수님"
        }
        response1 = client.post(url,
                               data=data1,
                               headers=self.get_auth_header(self.guest1.token))
        assert response1.status_code == 400

        data2 = copy.deepcopy(data1)
        data2["publisher_id"] = "1001"
        response2 = client.post(url,
                                data=data2,
                                headers=self.get_auth_header(self.guest1.token))
        assert response2.status_code == 400
