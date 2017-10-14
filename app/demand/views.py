from flask import g, jsonify, request

from app.application import db
from app.blueprints import demand

from .models import MeetingDemand
from .schemas import MeetingDemandSchema


@demand.route('/meeting/create', methods=["POST"])
def meeting_create():
    result, errors = MeetingDemandSchema().load(request.form)
    if errors:
        data = {"errors": errors}
        return jsonify(data), 400
    meeting_demand = MeetingDemand(**result, signaler_id=g.user.id,)
    db.session.add(meeting_demand)
    db.session.commit()
    schema = MeetingDemandSchema().dump(meeting_demand)
    return jsonify(schema.data), 201
