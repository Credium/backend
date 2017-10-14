import os
import time

from flask import current_app
from PIL import Image

base_image = Image.new('RGB', (100, 100))

def save_image(folder_name='', file_name='', image=None):
    image = image if image is not None else base_image
    media_path = current_app.config["MEDIA_FILE_PATH"]
    currently = time.strftime("%y%m%d%H%M%S")
    file_name = file_name + "_" + currently + ".jpg"
    save_path = os.path.join(media_path, folder_name, file_name)
    image.save(save_path)
    return save_path
