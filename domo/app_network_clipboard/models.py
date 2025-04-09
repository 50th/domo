import uuid

from django.db import models
from django.contrib.auth.models import User

from constants.constants import ClipboardPrivacy


class Clipboard(models.Model):
    """剪切板元数据模型"""
    clipboard_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    privacy_type = models.IntegerField(choices=ClipboardPrivacy.to_choices(), default=ClipboardPrivacy.private.value)
    password = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    created_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'clipboard'
