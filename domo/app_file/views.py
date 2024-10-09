import logging
import traceback
import urllib.parse
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.db.models.functions import Lower
from django.http import FileResponse, Http404
from rest_framework import mixins, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_file.models import File, FileDownloadLog
from app_file.serializers import FileSerializer

logger = logging.getLogger(__name__)


class CaseInsensitiveOrderingFilter(filters.OrderingFilter):
    """自定义排序类，指定字段排序不区分大小写"""

    def filter_queryset(self, request, queryset, view):

        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            new_ordering = []
            for field in ordering:
                if hasattr(view, 'case_insensitive_ordering_fields') and field in view.case_insensitive_ordering_fields:
                    if field.startswith('-'):
                        new_ordering.append(Lower(field[1:]).desc())
                    else:
                        new_ordering.append(Lower(field).asc())
                else:
                    new_ordering.append(field)
            return queryset.order_by(*new_ordering)
        return queryset


class FileDownloadCountView(APIView):
    """"""
    authentication_classes = [JWTAuthentication]  # 默认使用 jwt 认证
    permission_classes = []

    def get(self, request):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                queryset = File.objects.all()
            else:
                queryset = File.objects.filter(Q(upload_user=None) | Q(upload_user=request.user))
        else:
            queryset = File.objects.filter(upload_user=None)
        # annotate https://docs.djangoproject.com/zh-hans/5.1/topics/db/aggregation/#following-relationships-backwards
        # 使用 annotate 查询文件的下载量
        top_download_files = queryset.annotate(download_count=Count('filedownloadlog')).order_by('-download_count')[:5]
        top_download_files = FileSerializer(top_download_files, many=True)
        return Response({'top_download_files': top_download_files.data})


class FileViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = File.objects.all()
    filter_backends = [filters.SearchFilter, CaseInsensitiveOrderingFilter]
    search_fields = ('filename',)  # 搜索字段
    ordering_fields = ('upload_time', 'file_size', 'filename')
    case_insensitive_ordering_fields = ('filename',)
    serializer_class = FileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        user = self.request.user  # type: User
        if user and user.is_authenticated:
            if not user.is_superuser:
                queryset = queryset.filter(Q(upload_user=None) | Q(upload_user=user))
        else:
            queryset = queryset.filter(upload_user=None)
        return queryset.order_by('-upload_time')

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # type: File
        except Http404:
            response = Response(3000)
        else:
            if Path(instance.file_path.path).exists():
                if settings.DEV is True:
                    response = FileResponse(instance.file_path.open('rb'), as_attachment=True,
                                            filename=instance.filename)
                else:
                    # 正式环境配置跳转，由 nginx 负责下载
                    headers = {
                        'X-Accel-Redirect': f'/{urllib.parse.quote(str(instance.file_path))}',
                        'X-Accel-Buffering': 'yes',
                        'Content-Type': 'application/octet-stream',
                        'Content-Disposition': f'attachment; filename={urllib.parse.quote(instance.filename)}'
                    }
                    logger.info('response headers: %s', headers)
                    response = Response(status=200, headers=headers,
                                        content_type='application/octet-stream')
                download_log = FileDownloadLog.objects.create(
                    file=instance,
                    user=request.user if not request.user.is_anonymous else None,
                    user_ip=request.META['CLIENT_IP'],
                )
                download_log.save()
            else:
                response = Response(3000)
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # type: FileSerializer
        serializer.is_valid(raise_exception=True)
        # 非登录用户限制上传文件大小
        user = request.user
        file_size = serializer.validated_data['file_path'].size
        if not user.is_authenticated and file_size > settings.FILE_APP.get('MAX_FILE_SIZE'):
            return Response(3001)
        # 记录上传文件用户
        if user and user.is_authenticated:
            serializer.validated_data['upload_user'] = user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # type: File
            # 在 get_queryset 中已经过滤，只有公共文件或登录用户为文件所有人或登录用户是超级用户可以删除文件
            instance.file_path.delete()  # 删除默认会 save 一次，如果在删除对象后再删除文件会导致重新创建对象，一定要在删除对象前删除文件
            self.perform_destroy(instance)
        except Http404:
            pass
        except Exception as e:
            logger.error('destroy file error: %s', e)
            logger.error('destroy file error: %s', traceback.format_exc())
            return Response(3)
        return Response(0)
