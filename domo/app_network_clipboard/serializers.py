from rest_framework import serializers

from app_network_clipboard.models import Clipboard
from constants.constants import ClipboardPrivacy


class ClipboardSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=False)
    created_username = serializers.ReadOnlyField(source='created_user.username', default='')
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    def validate(self, attrs):
        privacy_type = attrs['privacy_type']
        password = attrs['password']
        if privacy_type == ClipboardPrivacy.shared_pass.value:
            if password is None or not password.strip():
                raise serializers.ValidationError('当选择使用密码共享时，密码不能为空')
            if len(password) < 6:
                raise serializers.ValidationError('当选择使用密码共享时，密码长度不能小于6位')
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.name is None or not instance.name.strip():
            instance.name = instance.clipboard_id
            instance.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data['privacy_type'] != ClipboardPrivacy.shared_pass.value:
            validated_data['password'] = None
        return super().update(instance, validated_data)

    class Meta:
        model = Clipboard
        fields = ['clipboard_id', 'name', 'privacy_type', 'password', 'content', 'created_user', 'created_username',
                  'created_time']
        read_only_fields = ['clipboard_id', 'created_user', 'created_username', 'created_time']
