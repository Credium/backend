from flask import g, jsonify, request

from app.account.permissions import publisher_required
from app.application import db
from app.blueprints import demand

from .models import MeetingDemand
from .schemas import MeetingDemandSchema


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
