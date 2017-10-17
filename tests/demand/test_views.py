import copy

import pytest
from flask import url_for


class TestMeetingDemandView:

    @classmethod
    @pytest.fixture(autouse=True)
    def setUp(self, db, guest1, publisher1):
        self.db = db
        self.guest1 = guest1
        self.publisher1 = publisher1

    def get_auth_header(self, token):
        return {
            "Authorization": token
        }

    def test_success_meeting_demand_create(self, client):
        url = url_for('demand.meeting_demand_create')
        data = {
            "publisher_id": self.publisher1.id,
            "title": "바둑 배우고 싶어요",
            "introduce": "바둑 1년 째 실력이 전혀 안늘어요ㅠ 도와주세여. 고수님"
        }
        response = client.post(url,
                               data=data,
                               headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 201
        assert response.json["title"] == "바둑 배우고 싶어요"

    def test_fail_meeting_demand_create(self, client):
        url = url_for('demand.meeting_demand_create')
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

    def test_receive_meetings_check(self, client):
        self.test_success_meeting_demand_create(client)
        url = url_for("demand.receive_meeting")
        response = client.get(url, headers=self.get_auth_header(self.publisher1.token))
        assert response.status_code == 200
        assert response.json[0]["id"] == 1

    def test_denied_meetings_request(self, client):
        url = url_for("demand.receive_meeting")
        response = client.get(url, headers=self.get_auth_header(self.guest1.token))
        assert response.status_code == 401

    def test_person_demand_create(self, client):
        url = url_for("demand.person_demand_create")
        data = {
            "full_name": "김수현",
            "job": "연애인",
            "description": "잘생김, ㄹㅇ 잘생김",
            "reference_link": "없떠 그런거"
        }
        response = client.post(url,
                               data=data)
        assert response.status_code == 201
        assert response.json["full_name"] == "김수현"
