from . import account
from .forms import LoginForm


@account.route('/login', methods=["POST"])
def login():
    form = LoginForm()
    if form.validate():
        return "validate"
    return "invalidate"
