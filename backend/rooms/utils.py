import os

from django.utils.text import slugify


def room_image_upload_path(instance, filename):
    """Формирует путь и имя файла для фотографии номера"""
    file_extension = filename.split('.')[-1]
    room_name = slugify(instance.room.title)
    count_images = instance.room.images.count()
    number_image = count_images + 1
    new_filename = f'{room_name}_{number_image}.{file_extension}'
    return os.path.join('room_images', room_name, new_filename)
