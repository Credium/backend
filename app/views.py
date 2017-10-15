import os
from flask import flash, g, jsonify, redirect, request, url_for, send_from_directory
from flask_admin import AdminIndexView as _AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView as _ModelView
from flask_login import current_user, login_required, login_user, logout_user

from app.account.forms import LoginForm
from app.account.models import User


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


def get_image(file_path):
    basedir = os.path.abspath(os.path.dirname(__file__))
    mediadir = os.path.join(basedir, "media")
    full_path = os.path.join(mediadir, file_path)

    if not os.path.exists(full_path):
        return jsonify({"error": "file doesn't exist"}), 404

    filedir, filename = os.path.split(full_path)
    return send_from_directory(filedir,
                               filename,
                               as_attachment=True,
                               mimetype="image/jpg")


def get_user_token():
    g.user = None
    token = request.headers.get("Authorization", None)
    if token is not None:
        user = User.query.filter_by(token=token).first()
        if user is None:
            return jsonify({"status": False, "error": "token is not valid"}), 401
        g.user = user
