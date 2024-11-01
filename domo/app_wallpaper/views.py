import logging
import traceback
import urllib.parse
import uuid
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from django.db.models import Q
from django.http import Http404, FileResponse
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_wallpaper.models import Wallpaper
from app_wallpaper.serializers import WallpaperSerializer
from constants.reponse_codes import ResponseCode
from utils.common_funcs import generate_file_md5
from utils.image_manager import ImageFile

logger = logging.getLogger(__name__)


def create_image_path(img_name: str) -> Path:
    """
    创建文件保存路径
    :param img_name: 文件名
    """
    image_dir = settings.WALLPAPER_APP.get('SAVE_DIR') / datetime.now().strftime('%Y-%m-%d')
    if not image_dir.exists():
        image_dir.mkdir(parents=True)
    image_path = image_dir / img_name
    return image_path


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_wallpaper(request):
    """壁纸上传"""
    image = request.FILES.get('wallpaper')  # type: TemporaryUploadedFile | InMemoryUploadedFile
    if not image:
        return Response(ResponseCode.PARAM_MISSING)
    if image.size > settings.WALLPAPER_APP.get('MAX_SIZE'):
        return Response(ResponseCode.WALLPAPER_TOO_LARGE)
    try:
        # 计算图片的 md5 值，检查图片是否已经存在
        source_img_hash = generate_file_md5(image)
        exist_wallpaper = Wallpaper.objects.filter(Q(source_image_hash=source_img_hash) | Q(image_hash=source_img_hash))
        if exist_wallpaper:
            return Response(ResponseCode.WALLPAPER_EXIST)
        else:
            image.seek(0)
            with ImageFile(image) as img:
                if img.is_image():
                    img_id = uuid.uuid4().hex
                    img_name = f'{img_id}.jpg'
                    img_path = create_image_path(img_name)
                    img.convert_image_format(img_path)
                    with open(img_path, 'rb') as f:
                        img_hash = generate_file_md5(f)
                    user = request.user if request.user and request.user.is_authenticated else None
                    Wallpaper.objects.create(id=img_id, image_name=img_name, image_size=img_path.stat().st_size,
                                             image_path=img_path, image_width=img.width, image_height=img.height,
                                             source_image_hash=source_img_hash, image_hash=img_hash, upload_user=user)
                    # 保存缩略图
                    if not settings.WALLPAPER_APP.get('THUMB_SAVE_DIR').exists():
                        settings.WALLPAPER_APP.get('THUMB_SAVE_DIR').mkdir(parents=True)
                    img.save_thumb(settings.WALLPAPER_APP.get('THUMB_SAVE_DIR') / img_name)
                    return Response(ResponseCode.OK)
                else:
                    return Response(ResponseCode.PARAM_ERROR)
    except Exception as e:
        logger.error('upload_wallpaper error: %s', e)
        return Response(ResponseCode.SERVER_EXCEPTION)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def wallpaper_thumb(request, wallpaper_id: str):
    """缩略图请求"""
    if not wallpaper_id:
        return Response(ResponseCode.PARAM_MISSING)
    wallpaper = Wallpaper.objects.filter(id=wallpaper_id).first()
    if wallpaper:
        thumb_path = settings.WALLPAPER_APP.get('THUMB_SAVE_DIR') / wallpaper.image_name
        if thumb_path.exists():
            if settings.DEV is True:
                response = FileResponse(open(thumb_path, 'rb'), as_attachment=True, filename=wallpaper.image_name,
                                        content_type='application/octet-stream')
            else:
                # 正式环境配置跳转，跳转到 nginx 负责下载
                headers = {
                    'X-Accel-Redirect': f'/{urllib.parse.quote(str(thumb_path))}',
                    'X-Accel-Buffering': 'yes',
                    'Content-Type': 'application/octet-stream',
                    'Content-Disposition': f'attachment; filename={urllib.parse.quote(wallpaper.image_name)}'
                }
                response = Response(status=200, headers=headers, content_type='application/octet-stream')
            return response
        else:
            return Response(ResponseCode.WALLPAPER_NOT_EXIST)
    else:
        return Response(ResponseCode.WALLPAPER_NOT_EXIST)


class WallpaperViewSet(mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Wallpaper.objects.all().order_by('-upload_time')
    serializer_class = WallpaperSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # type: Wallpaper
        except Http404:
            logger.info('wallpaper not exist: %s', kwargs.get('id'))
            response = Response(ResponseCode.WALLPAPER_NOT_EXIST)
        else:
            if Path(instance.image_path).exists():
                if settings.DEV is True:
                    response = FileResponse(open(instance.image_path, 'rb'), as_attachment=True,
                                            filename=instance.image_name, content_type='application/octet-stream')
                else:
                    # 正式环境配置跳转，由 nginx 负责下载
                    headers = {
                        'X-Accel-Redirect': f'/{urllib.parse.quote(instance.image_path)}',
                        'X-Accel-Buffering': 'yes',
                        'Content-Type': 'application/octet-stream',
                        'Content-Disposition': f'attachment; filename={urllib.parse.quote(instance.image_name)}'
                    }
                    logger.info('response headers: %s', headers)
                    response = Response(status=200, headers=headers, content_type='application/octet-stream')
                # download_log = FileDownloadLog.objects.create(
                #     file=instance,
                #     user=request.user if not request.user.is_anonymous else None,
                #     user_ip=request.META['CLIENT_IP'],
                # )
                # download_log.save()
            else:
                logger.info('wallpaper file not exist: %s', instance.image_path)
                response = Response(ResponseCode.WALLPAPER_NOT_EXIST)
        return response

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # type: Wallpaper
            # 在 get_queryset 中已经过滤，只有公共文件或登录用户为文件所有人或登录用户是超级用户可以删除文件
            image_path = Path(instance.image_path)
            self.perform_destroy(instance)
            if image_path.exists():
                image_path.unlink()
            # 删除缩略图
            thumb_path = settings.WALLPAPER_APP.get('THUMB_SAVE_DIR') / instance.image_name
            if thumb_path.exists():
                thumb_path.unlink()
            # 删除空目录
            if image_path.parent.exists() and len(list(image_path.parent.iterdir())) == 0:
                image_path.parent.rmdir()
        except Http404:
            logger.info('destroy file not exist')
        except Exception as e:
            logger.error('destroy file error: %s', e)
            logger.error('destroy file error: %s', traceback.format_exc())
            return Response(ResponseCode.SERVER_EXCEPTION)
        return Response(ResponseCode.OK)
