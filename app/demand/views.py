from flask import g, jsonify, request

from app.account.permissions import publisher_required
from app.application import db
from app.blueprints import demand

from .models import MeetingDemand, PersonDemand
from .schemas import MeetingDemandSchema, PersonDemandSchema
from app.helpers import save_image


@demand.route('/meeting', methods=["POST"])
def meeting_demand_create():
    result, errors = MeetingDemandSchema().load(request.form)
    if errors:
        data = {"errors": errors}
        return jsonify(data), 400
    meeting_demand = MeetingDemand(**result, signaler_id=g.user.id,)
    db.session.add(meeting_demand)
    db.session.commit()
    schema = MeetingDemandSchema().dump(meeting_demand)
    return jsonify(schema.data), 201


@demand.route('/meeting', methods=["GET"])
@publisher_required
def receive_meeting():
    demanded_meetings = MeetingDemand.query.filter_by(publisher=g.user.publisher_info)
    schema = MeetingDemandSchema(exclude=("publisher", ), many=True).dump(demanded_meetings)
    return jsonify(schema.data), 200


@demand.route("/person", methods=["POST"])
def person_demand_create():
    full_name = request.form.get("full_name", "")
    image = request.files.get("profile_photo", None)
    photo_path = save_image("user_profile", full_name, image)
    request_data = request.form.to_dict()
    request_data["profile_photo_path"] = photo_path
    result, errors = PersonDemandSchema().load(request_data)
    if errors:
        data = {"errors": errors}
        return jsonify(data), 400
    person_demand = PersonDemand(**result)
    db.session.add(person_demand)
    db.session.commit()
    schema = PersonDemandSchema().dump(person_demand)
    return jsonify(schema.data), 201
