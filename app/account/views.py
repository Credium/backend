from . import account
from .forms import LoginForm


@account.route('/login', methods=["POST"])
def login():
    # todo 로그인
    form = LoginForm()
    if form.validate():
        return "validate"
    return "invalidate"


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
