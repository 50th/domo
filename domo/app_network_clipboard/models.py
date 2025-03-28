import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from constants.constants import ClipboardPrivacy, ClipboardContentType


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


class ClipboardContent(models.Model):
    """剪切板内容模型"""
    content_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clipboard = models.ForeignKey(Clipboard, on_delete=models.CASCADE, related_name='contents')
    content_type = models.IntegerField(choices=ClipboardContentType.to_choices(), default=ClipboardContentType.text.value)
    text_content = models.TextField(blank=True, null=True)
    file_metadata = JSONField(blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
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
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('admin', 'Admin')
    ]

    share_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clipboard = models.ForeignKey(Clipboard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_level = models.CharField(max_length=20, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('clipboard', 'user')
        indexes = [
            models.Index(fields=['clipboard', 'permission_level']),
        ]

    def __str__(self):
        return f"Share {self.clipboard.name} with {self.user.username}"
