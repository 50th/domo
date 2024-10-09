import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


def create_file_path(instance: models.FileField, filename: str):
    """
    创建文件保存路径

    :param instance: models.FileField 对象
    :param filename: 文件名
    """
    file_dir = settings.FILE_APP.get('FILE_SAVE_DIR') / datetime.now().strftime('%Y-%m-%d')
    if not file_dir.exists():
        file_dir.mkdir(parents=True)
    file_path = file_dir / f'{filename}.{uuid.uuid4().hex}'
    return file_path


class File(models.Model):
    """文件模型"""
    filename = models.CharField(max_length=128, null=False, blank=True, verbose_name='文件名')
    file_size = models.IntegerField(null=False, blank=True, verbose_name='文件大小(bytes)')
    file_type = models.CharField(max_length=64, null=False, blank=True, verbose_name='文件类型')
    file_path = models.FileField(upload_to=create_file_path, null=False, verbose_name='文件')
    upload_time = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name='上传时间')
    upload_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, verbose_name='上传人')

    def __str__(self):
        return f'{self.filename}_{self.file_size}_{self.upload_time}'

    class Meta:
        db_table = 'file'


class FileDownloadLog(models.Model):
    """文件下载记录"""
    file = models.ForeignKey(File, null=True, on_delete=models.SET_NULL, verbose_name='文件')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='用户')
    user_ip = models.CharField(max_length=128, verbose_name='用户 IP')
    download_time = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name='下载时间')

    def __str__(self):
        return f'{self.file.filename}_{self.user.username}_{self.download_time}'

    class Meta:
        db_table = 'file_download_log'
