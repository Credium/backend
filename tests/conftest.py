import pytest

from app.account.models import User
from app.application import db as _db
from app.application import create_app
import os
from PIL import Image


@pytest.yield_fixture(scope="session")
def app():
    app = create_app('testing')
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.yield_fixture(scope="function")
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture(autouse=True)
def admin_user(app, db):
    image = Image.new('RGB', (100, 100))
    save_path = os.path.join(app.config["MEDIA_FILE_PATH"], "user_profile", "image03.jpg")
    image.save(save_path)
    admin_user = User(username="admin",
                      password="admin",
                      type="admin",
                      profile_photo_path=save_path,
                      job="의사선생님",
                      phone_number="01099725801",
                      full_name="김의사"
                      )
    db.session.add(admin_user)
    db.session.commit()
    yield admin_user
    os.remove(save_path)
