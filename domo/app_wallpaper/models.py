import uuid

from django.contrib.auth.models import User
from django.db import models


class Wallpaper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_name = models.CharField(max_length=64, verbose_name='图片名')
    image_size = models.IntegerField(null=False, blank=True, verbose_name='图片大小(bytes)')
    image_path = models.CharField(max_length=100, null=False, blank=True, verbose_name='图片路径')
    image_width = models.IntegerField(null=False, blank=True, verbose_name='图片宽度')
    image_height = models.IntegerField(null=False, blank=True, verbose_name='图片高度')
    source_image_hash = models.CharField(max_length=64, null=False, blank=True, verbose_name='原始图片哈希值')
    image_hash = models.CharField(max_length=64, null=False, blank=True, verbose_name='保存图片哈希值')
    upload_time = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name='上传时间')
    upload_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, verbose_name='上传人')

    class Meta:
        db_table = 'wallpaper'
