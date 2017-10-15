from flask import g, jsonify, request

from app.application import db
from app.blueprints import account
from app.helpers import save_image

from .models import User
from .schemas import LoginSchema, UserSchema
from .permissions import login_required
from  sqlalchemy.sql.expression import func


@account.route('/login', methods=["POST"])
def login():
    data, errors = LoginSchema().load(request.form)
    if errors:
        return jsonify(errors), 401
    return jsonify(data["user"].data)


@account.route('/logout', methods=["GET"])
def logout():
    if g.user is not None:
        g.user.change_token()
    return jsonify({"status": True})


@account.route('/', methods=["POST"])
def register():
    username = request.form.get("username", "")
    image = request.files.get("profile_photo", None)
    photo_path = save_image("user_profile", username, image)
    request_data = request.form.to_dict()
    request_data["profile_photo_path"] = photo_path
    data, errors = UserSchema().load(request_data)
    if errors:
        data = {"errors": errors}
        return jsonify(data), 400
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    data, errors = UserSchema(many=False).dump(user)
    return jsonify(data), 201


@account.route('/', methods=["DELETE"])
@login_required
def delete():
    db.session.delete(g.user)
    db.session.commit()
    return jsonify({"status": True}), 200


@account.route('/', methods=["PUT"])
@login_required
def update():
    # todo: form으로 update data의 validate()수행
    g.user.username = request.form.get("username")
    g.user.password_hash = request.form.get("password")
    db.session.commit()
    return jsonify({"status": True}), 200


@account.route('/', methods=["GET"])
@login_required
def user_info():
    data, errors = UserSchema().dump(g.user)
    return jsonify(data), 200


@account.route("/recommend_publisher", methods=["GET"])
def recommend_publisher():
    # todo 지금은 랜덤으로 조회하지만 나중에는 적절한 근거에 입각하여 추천
    publishers = User.query.filter_by(type="publisher")\
                     .order_by(func.random()).all()[0:5]
    schema = UserSchema().dump(publishers, many=True)
    return jsonify(schema.data)
