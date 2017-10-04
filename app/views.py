from flask_login import login_user, current_user, login_required, logout_user
from flask import flash, redirect, url_for
from flask_admin import AdminIndexView as _AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView as _ModelView

from app.account.forms import LoginForm


class AdminIndexView(_AdminIndexView):

    @expose('/', methods=["GET"])
    def index(self):
        form = LoginForm()
        self._template_args["form"] = form
        return super(AdminIndexView, self).index()

    @expose('/login/', methods=["POST"])
    def login(self):
        form = LoginForm()
        if not form.validate():
            flash("form is not valid")
            return redirect(url_for('.index'))

        user = form.auth()
        if user is None:
            flash("login fail")
            return redirect(url_for('.index'))

        login_user(user)
        flash("login success")
        return redirect(url_for('.index'))

    @expose('/logout/', methods=["POST"])
    @login_required
    def logout(self):
        logout_user()
        flash("logout success")
        return redirect(url_for('.index'))


class ModelView(_ModelView):

    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.is_superuser
