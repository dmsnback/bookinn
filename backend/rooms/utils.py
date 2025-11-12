import os
from datetime import datetime

from slugify import slugify


def room_image_upload_path(instance, filename):
    """Формирует путь и имя файла для фотографии номера"""
    file_extension = filename.split('.')[-1]
    room_name = slugify(instance.room.title, lowercase=True) or 'room'
    upload_date = datetime.now().strftime('%Y-%m-%d_%H-%M')
    count_image = instance.room.images.count()
    number_image = count_image + 1
    new_filename = f'{room_name}_{upload_date}_{number_image}.{file_extension}'
    return os.path.join('room_images', room_name, new_filename)
