import logging

from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import serializers

from app_video.models import Video
from utils.common_funcs import check_file_type
from utils.video_operator import VideoOperator

logger = logging.getLogger(__name__)


class VideoSerializer(serializers.ModelSerializer):
    video_path = serializers.FileField(write_only=True)  # 序列化时不返回字段
    video_res = serializers.SerializerMethodField(read_only=True)
    upload_username = serializers.ReadOnlyField(source='upload_user.username', default='')
    upload_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    def get_video_res(self, obj: Video):
        if obj.video_width and obj.video_height:
            return f'{obj.video_width} x {obj.video_height}'
        else:
            return '-'

    def create(self, validated_data):
        video = validated_data['video_path']  # type: TemporaryUploadedFile
        # 使用 magika 判断文件类型
        video_type = check_file_type(video)
        validated_data['video_name'] = video.name
        validated_data['video_size'] = video.size
        validated_data['video_type'] = video_type
        validated_data['upload_user'] = self.context['request'].user
        video_obj = super().create(validated_data)  # type: Video
        # 使用 ffmpeg 获取视频时长
        try:
            vo = VideoOperator(video_obj.video_path.path)
        except Exception as e:
            logger.error('get video duration fail: %s', e)
            video_obj.video_path.delete()
            video_obj.delete()
            raise e
        else:
            if vo.video_info:
                video_obj.video_duration = vo.video_info.duration_seconds
                video_obj.video_bitrate = vo.video_info.bitrate
                video_obj.video_width = vo.video_info.width
                video_obj.video_height = vo.video_info.height
                video_obj.save(update_fields=['video_duration', 'video_bitrate', 'video_width', 'video_height'])
        return video_obj

    class Meta:
        model = Video
        fields = ['id', 'video_uuid', 'video_name', 'video_path', 'video_size', 'video_duration', 'video_res',
                  'video_bitrate', 'video_type', 'upload_user', 'upload_username', 'upload_time']
        read_only_fields = ['id', 'video_uuid', 'video_name', 'video_path', 'video_size', 'video_duration', 'video_res',
                            'video_bitrate', 'video_type', 'upload_user', 'upload_username', 'upload_time']
