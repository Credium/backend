import os
import time

from flask import current_app
from marshmallow import ValidationError, fields, validates
from PIL import Image

from app.account.models import User

base_image = Image.new('RGB', (100, 100))

def save_image(folder_name='', file_name='', image=None):
    image = image if image is not None else base_image
    media_path = current_app.config["MEDIA_FILE_PATH"]
    currently = time.strftime("%y%m%d%H%M%S")
    file_name = file_name + "_" + currently + ".jpg"
    save_path = os.path.join(media_path, folder_name, file_name)
    image.save(save_path)
    return save_path


class PublisherIDSchemaMixin:
    publisher_id = fields.Method(load_only=True, deserialize="load_publisher_id")

    @validates("publisher_id")
    def validate_publisher_id(self, value):
        if value is None:
            raise ValidationError("publisher id is not exist or publisher")

    def load_publisher_id(self, value):
        publisher = User.query.filter_by(id=value).first()
        if publisher is not None and publisher.is_publisher:
            return publisher.publisher_info.id
        else:
            return None