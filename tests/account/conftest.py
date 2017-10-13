import os

import pytest
from PIL import Image

from app.account.models import User


@pytest.fixture(autouse=True)
def guest1(app, db):
    image = Image.new('RGB', (100, 100))
    save_path = os.path.join(app.config["MEDIA_FILE_PATH"], "user_profile", "image01.jpg")
    image.save(save_path)
    user = User(username="guest1",
                password="guest1",
                type="signaler",
                profile_photo_path=save_path,
                job="의사선생님",
                phone_number="01099725801",
                full_name="김의사"
                )
    db.session.add(user)
    db.session.commit()
    yield user
    os.remove(save_path)


@pytest.fixture(autouse=True)
def dict_guest2(app, db):
    image = Image.new('RGB', (100, 100))
    save_path = os.path.join(app.config["MEDIA_FILE_PATH"], "image02.png")
    image.save(save_path)
    dict_user = dict(username="guest2",
                     password="guest2",
                     type="signaler",
                     profile_photo_path=save_path,
                     job="의사선생님",
                     phone_number="01099725801",
                     full_name="김의사"
                     )
    return dict_user
