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
    content = models.TextField(blank=True, null=True)
    created_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def is_accessible_by_user(self, user, password=None):
        """
        检查剪切板项是否可以被给定的用户访问。
        """
        if self.privacy_type == ClipboardPrivacy.private.value:
            return self.created_user == user
        elif self.privacy_type == ClipboardPrivacy.shared_no_pass.value:
            return True  # 所有用户都可以访问共享剪切板
        elif self.privacy_type == ClipboardPrivacy.shared_pass.value and password:
            return self.password == password  # 检查密码是否匹配
        return False

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'clipboard'
