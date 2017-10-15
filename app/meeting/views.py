from app.blueprints import meeting
from flask import g, jsonify, request

from app.application import db

from .models import Meeting, Participate
from .schemas import MeetingSchema
from app.account.permissions import publisher_required
from app.account.models import PublisherInfo


@meeting.route('/', methods=["POST"])
@publisher_required
def meeting_create():
    result, errors = MeetingSchema().load(request.form)
    if errors:
        data = {"errors": errors}
        return jsonify(data), 400
    meeting = Meeting(**result, publisher_id=g.user.publisher_info.id)
    db.session.add(meeting)
    db.session.commit()
    schema = MeetingSchema().dump(meeting)
    return jsonify(schema.data), 201


@meeting.route("/", methods=["GET"])
def get_all_meetings():
    meetings = Meeting.query.all()
    schema = MeetingSchema(many=True).dump(meetings)
    return jsonify(schema.data), 200


@meeting.route("/<int:publisher_id>", methods=["GET"])
def get_publisher_meetings(publisher_id):
    schema, errors = MeetingSchema(only=("publisher_id", )).load({"publisher_id":publisher_id})
    if errors:
        data = {"errors": errors}
        return jsonify(data), 400
    publisher = PublisherInfo.query.filter_by(user_id=publisher_id).first()
    schema = MeetingSchema(exclude=("publisher", ), many=True).dump(publisher.make_meetings)
    return jsonify(schema.data), 200
