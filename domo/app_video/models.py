import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def create_file_path(instance: models.FileField, filename: str):
    """
    创建文件保存路径

    :param instance: models.FileField 对象
    :param filename: 文件名
    """
    file_dir = settings.VIDEO_APP.get('VIDEO_DIR') / datetime.now().strftime('%Y-%m-%d')
    if not file_dir.exists():
        file_dir.mkdir(parents=True)
    file_path = file_dir / f'{filename}.{uuid.uuid4().hex}'
    return file_path


class Video(models.Model):
    """视频模型"""
    video_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    video_name = models.CharField(max_length=128, null=False, blank=True, verbose_name='视频名称')
    video_size = models.IntegerField(null=False, blank=True, verbose_name='文件大小(bytes)')
    video_duration = models.IntegerField(null=True, blank=True, verbose_name='视频时间长度')
    video_type = models.CharField(max_length=64, null=False, blank=True, verbose_name='视频类型')
    video_path = models.FileField(upload_to=create_file_path, null=False, verbose_name='文件')
    upload_time = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name='上传时间')
    upload_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, verbose_name='上传人')

    def __str__(self):
        return f'{self.video_name}_{self.video_size}_{self.upload_time}'

    class Meta:
        db_table = 'video'
