import os
import time

from flask import current_app, request
from marshmallow import ValidationError, fields, validates
from PIL import Image

from app.account.models import User

base_image = Image.new('RGB', (100, 100))


def save_image(folder_name='', file_name='', image=None):
    image = image if image is not None else base_image
    media_path = current_app.config["MEDIA_FILE_PATH"]
    currently = time.strftime("%y%m%d%H%M%S")
    file_name = file_name + "_" + currently + ".jpg"
    direcotry_path = os.path.join(media_path, folder_name)
    if not os.path.isdir(direcotry_path):
        os.makedirs(direcotry_path)
    save_path = os.path.join(direcotry_path, file_name)
    image.save(save_path)
    return os.path.join(folder_name, file_name)


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


def pagination_value_parser():
    return request.args.get("max_id", 0), request.args.get("count", 15)


def pagination_query(Query, max_id=None, count=15):
    query = Query.query
    if max_id is None:
        return query.limit(count)

    return query.filter(Query.id < max_id).limit(count)
