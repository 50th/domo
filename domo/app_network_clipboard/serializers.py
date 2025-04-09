from rest_framework import serializers

from app_network_clipboard.models import Clipboard
from constants.constants import ClipboardPrivacy


class ClipboardSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    def validate(self, attrs):
        privacy_type = attrs['privacy_type']
        password = attrs['password']
        if privacy_type == ClipboardPrivacy.shared_pass.value and (password is None or not password.strip()):
            raise serializers.ValidationError('当选择使用密码共享时，密码不能为空')
        return attrs

    class Meta:
        model = Clipboard
        fields = '__all__'
