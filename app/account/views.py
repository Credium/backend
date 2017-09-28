from . import account
from .forms import LoginForm
from app import login_manager
from flask import jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@account.route('/login', methods=["POST"])
def login():
    form = LoginForm()
    if not form.validate():
        return jsonify({"ok": False, "error": "invalidated form"}), 405

    user = form.auth()
    if user is None:
        return jsonify({"ok": False, "error": "invalidated user"}), 405
    user.authenticated = True
    login_user(user, remember=True)
    return jsonify({"ok": True, "user": user.dict()}), 200


@account.route('/logout', methods=["POST"])
def logout():
    # todo 로그아웃
    pass


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
