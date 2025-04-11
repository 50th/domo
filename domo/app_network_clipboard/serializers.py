from rest_framework import serializers

from app_network_clipboard.models import Clipboard
from constants.constants import ClipboardPrivacy


class ClipboardSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    created_username = serializers.ReadOnlyField(source='created_user.username', default='')
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    def create(self, validated_data):
        """name 为空时，将 id 作为 name"""
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
