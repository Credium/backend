from flask import g, jsonify, request

from app.application import db
from app.blueprints import account

from .forms import RegisterForm
from .schemas import LoginSchema
from .models import User


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


@account.route('/register', methods=["POST"])
def register():
    form = RegisterForm(request.form)
    if not form.validate():
        return jsonify({"status": False, "error": "invalidated form"}), 400

    user = User(username=form.username.data,
                password=form.password.data)
    db.session.add(user)
    db.session.commit()

    return jsonify({"status": True, "user": user.dict()}), 201


@account.route('/delete', methods=["DELETE"])
def delete():
    db.session.delete(g.user)
    db.session.commit()
    return jsonify({"status": True}), 200


@account.route('/update', methods=["PUT"])
def update():
    # todo: form으로 update data의 validate()수행
    g.user.username = request.form.get("username")
    g.user.password_hash = request.form.get("password")
    db.session.commit()
    return jsonify({"status": True}), 200


@account.route('/user-info', methods=["GET"])
def user_info():
    return jsonify({"status": True, "user": g.user.dict()}), 200
