from app.blueprints import meeting
from flask import g, jsonify, request

from app.application import db

from .models import Meeting, Participate
from .schemas import MeetingSchema


@meeting.route('/', methods=["POST"])
def meeting_create():
    if g.user.type != "publisher":
        data = {"error": "user is not publisher"}
        return jsonify(data), 403
    result, errors = MeetingSchema().load(request.form)
    if errors:
        data = {"errors": errors}
        return jsonify(data), 400
    meeting = Meeting(**result, publisher_id=g.user.publisher_info.id)
    db.session.add(meeting)
    db.session.commit()
    schema = MeetingSchema().dump(meeting)
    return jsonify(schema.data), 201


@meeting.route("/<int:publisher_id>", methods=["GET"])
def get_publisher_meetings():
    pass
