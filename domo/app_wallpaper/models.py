import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def create_image_path(instance: 'Wallpaper', filename: str):
    """
    创建文件保存路径

    :param instance: Wallpaper 对象
    :param filename: 文件名
    """
    file_dir = settings.FILE_APP.get('FILE_SAVE_DIR') / datetime.now().strftime('%Y-%m-%d')
    if not file_dir.exists():
        file_dir.mkdir(parents=True)
    file_path = file_dir / f'{instance.id}.jpeg'
    return file_path


class Wallpaper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_size = models.IntegerField(null=False, blank=True, verbose_name='图片大小(bytes)')
    image_path = models.FileField(upload_to=create_image_path, null=False, verbose_name='图片路径')
    # image_type = models.FileField(upload_to=create_image_path, null=False, verbose_name='图片路径')
    image_width = models.IntegerField(null=False, blank=True, verbose_name='图片宽度')
    image_height = models.IntegerField(null=False, blank=True, verbose_name='图片高度')
    upload_time = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name='上传时间')
    upload_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, verbose_name='上传人')

    class Meta:
        db_table = 'wallpaper'
