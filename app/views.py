import flask_login as login
from flask import flash, redirect, url_for
from flask_admin import AdminIndexView as _AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView as _ModelView

from app.account.forms import LoginForm


class AdminIndexView(_AdminIndexView):

    @expose('/')
    def index(self):
        form = LoginForm()
        self._template_args["form"] = form
        return super(AdminIndexView, self).index()

    @expose('/login/', methods=["POST"])
    def login(self):
        form = LoginForm()
        if not form.validate():
            flash("form is not valid")
        user = form.auth()
        print(user)
        if user is None:
            flash("login fail")
        else:
            login.login_user(user)
            flash("login success")
        return redirect(url_for('.index'))

    @expose('/logout/')
    def logout(self):
        return "logout"


class ModelView(_ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated
