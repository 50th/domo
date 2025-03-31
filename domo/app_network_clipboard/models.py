import uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from constants.constants import ClipboardPrivacy, ClipboardContentType, ClipboardSharePermission


class Clipboard(models.Model):
    """剪切板元数据模型"""
    clipboard_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    privacy_type = models.IntegerField(choices=ClipboardPrivacy.to_choices(), default=ClipboardPrivacy.private.value)
    password_hash = models.CharField(max_length=100, blank=True, null=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'clipboard'


def create_file_path(instance: 'ClipboardContent', filename: str):
    """
    创建文件保存路径

    :param instance: File 对象
    :param filename: 文件名
    """
    file_dir = settings.FILE_APP.get('FILE_SAVE_DIR') / datetime.now().strftime('%Y-%m-%d')
    if not file_dir.exists():
        file_dir.mkdir(parents=True)
    file_path = file_dir / f'{filename}.{uuid.uuid4().hex}'
    return file_path


class ClipboardContent(models.Model):
    """剪切板内容模型"""
    content_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clipboard = models.ForeignKey(Clipboard, on_delete=models.CASCADE, related_name='contents')
    content_type = models.IntegerField(choices=ClipboardContentType.to_choices(),
                                       default=ClipboardContentType.text.value)
    text_content = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    file_path = models.FileField(upload_to=create_file_path, blank=True, null=True)
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.clipboard.name} - {self.content_type}'

    class Meta:
        db_table = 'clipboard_content'
        indexes = [
            models.Index(fields=['clipboard', 'created_at']),
        ]


class ClipboardShare(models.Model):
    """剪切板共享模型"""
    share_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clipboard = models.ForeignKey(Clipboard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_level = models.IntegerField(choices=ClipboardSharePermission.to_choices(),
                                           default=ClipboardSharePermission.read.value)

    class Meta:
        db_table = 'clipboard_share'
        unique_together = ('clipboard', 'user')
        indexes = [
            models.Index(fields=['clipboard', 'permission_level']),
        ]

    def __str__(self):
        return f'Share {self.clipboard.name} with {self.user.username}'
