import logging

from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import serializers

from app_file.models import File
from utils.common_funcs import check_file_type

logger = logging.getLogger(__name__)


class FileSerializer(serializers.ModelSerializer):
    file_path = serializers.FileField(write_only=True)  # 序列化时不返回字段
    download_count = serializers.SerializerMethodField()
    upload_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    def get_download_count(self, obj: File) -> int:
        return obj.filedownloadlog_set.count()

    def create(self, validated_data):
        file = validated_data['file_path']  # type: TemporaryUploadedFile
        # 使用 magika 判断文件类型
        file_type = check_file_type(file)
        validated_data['filename'] = file.name
        validated_data['file_size'] = file.size
        validated_data['file_type'] = file_type
        return super().create(validated_data)

    class Meta:
        model = File
        fields = ['id', 'filename', 'file_path', 'file_size', 'file_type', 'upload_time', 'download_count']
        read_only_fields = ['id', 'filename', 'file_path', 'file_size', 'file_type', 'upload_time', 'download_count']
