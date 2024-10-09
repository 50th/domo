import logging
import os
import traceback
from pathlib import Path
from typing import Union

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse, HttpResponseNotFound, Http404
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_video.models import Video
from app_video.serializers import VideoSerializer

logger = logging.getLogger(__name__)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('video_name',)
    ordering = ['-upload_time']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user  # type: User
        if not user.is_superuser:
            queryset = queryset.filter(upload_user=user)
        return queryset.order_by('-upload_time')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # type: Video
            if instance.video_path:
                video_dir = Path(instance.video_path.path).parent
                instance.video_path.delete()  # 删除默认会 save 一次，如果在删除对象后再删除文件会导致重新创建对象，一定要在删除对象前删除文件
                # 检查目录是否还有其他文件，没有则删除目录
                if len(os.listdir(video_dir)) == 0:
                    video_dir.rmdir()
            self.perform_destroy(instance)
        except Http404:
            pass
        except Exception as e:
            logger.error('destroy file error: %s', e)
            logger.error('destroy file error: %s', traceback.format_exc())
            return Response(3)
        return Response(0)


def video_iterator(file_path: Union[str, Path], start_p: int, end_p: int, chunk_size: int = 512):
    with open(file_path, 'rb') as video_file:
        video_file.seek(start_p)
        while start_p <= end_p:
            chunk = video_file.read(min(chunk_size, end_p - start_p + 1))
            if not chunk:
                break
            yield chunk
            start_p += len(chunk)


def video_serve(request, video_uuid: str):
    try:
        instance = Video.objects.filter(video_uuid=video_uuid).first()
    except ValidationError:
        return HttpResponseNotFound('Video file not found')
    if not instance or not os.path.exists(instance.video_path.path):
        return HttpResponseNotFound('Video file not found')

    start = 0
    content_length = 1024 * 256  # 默认返回字节数
    end = None
    # 检查Range头部
    range_header = request.META.get('HTTP_RANGE')
    if range_header:
        # 解析 Range 值，示例: "bytes=0-499" 表示请求前500个字节
        _, range_str = range_header.split('=')
        ranges = range_str.split('-')
        if len(ranges) == 2:
            start = int(ranges[0])
            if ranges[1]:
                end = int(ranges[1])
                content_length = end - start + 1
    if not end:
        end = start + content_length - 1
    file_size = os.path.getsize(instance.video_path.path)
    if end >= file_size:
        end = file_size - 1
        content_length = end - start + 1
    response = StreamingHttpResponse(video_iterator(instance.video_path.path, start, end, 512), status=206)
    # 设置响应头部
    response['Content-Type'] = 'video/mp4'
    response['Content-Range'] = f'bytes {start}-{end}/{os.path.getsize(instance.video_path.path)}'
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = content_length
    return response
