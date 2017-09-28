from flask import g, jsonify, request

from . import account
from .forms import LoginForm
from .models import User


@account.before_request
def get_user_token():
    g.user = None
    token = request.headers.get("Authorization", None)
    if token is not None:
        user = User.query.filter_by(token=token).first()
        if user is None:
            return "token is not valid", 403
        g.user = user


@account.route('/login', methods=["POST"])
def login():
    form = LoginForm()
    if not form.validate():
        return jsonify({"ok": False, "error": "invalidated form"}), 405

    user = form.auth()
    if user is None:
        return jsonify({"ok": False, "error": "invalidated user"}), 405
    return jsonify({"ok": True, "user": user.dict()}), 200


@account.route('/logout', methods=["GET"])
def logout():
    if g.user is not None:
        g.user.change_token()
    return jsonify({"status": True})


@account.route('/register', methods=["POST"])
def register():
    # todo 유저 등록
    pass


@account.route('/delete', methods=["DELETE"])
def delete():
    # todo 유저 회원 탈퇴
    pass


@account.route('/update', methods=["PUT"])
def update():
    # todo 유저 정보 업데이트
    pass


@account.route('/user-info', methods=["GET"])
def user_info():
    # todo 토큰으로 유저 정보 반환
    pass
