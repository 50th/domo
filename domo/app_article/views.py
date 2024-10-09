import logging
import uuid

from django.conf import settings
from django.db.models import Q
from django.http import Http404
from rest_framework import permissions, viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_article.serializers import ArticleListSerializer, ArticleSerializer, UploadImgForm
from app_article.models import Article, ArticleEditLog, ArticleActivityLog
from constants.constants import ArticleStatus, ArticleActionType
from utils.common_funcs import generate_article, save_article_file

logger = logging.getLogger(__name__)


class ArticleViewCountView(APIView):
    """查询浏览量"""
    authentication_classes = [JWTAuthentication]  # 默认使用 jwt 认证
    permission_classes = []

    def get(self, request):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                queryset = Article.objects.all()
            else:
                queryset = Article.objects.filter(Q(status=ArticleStatus.display.value) | Q(author=request.user))
        else:
            queryset = Article.objects.filter(status=ArticleStatus.display.value)
        top_view_articles = queryset.order_by('-view_count')[:5]
        return Response({'top_view_articles': ArticleListSerializer(top_view_articles, many=True).data})


class ArticleImgView(APIView):
    """
    上传文章中的图片
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]  # 需要管理员权限

    def post(self, request):
        form = UploadImgForm(files=request.FILES)
        if form.is_valid():
            img = request.FILES['img']
            name, suffix = img.name.rsplit('.', 1)
            img_name = f'article_img_{uuid.uuid4()}.{suffix}'
            img_path = settings.ARTICLE_APP.get('IMG_SAVE_DIR') / img_name
            # 保存图片
            if not settings.ARTICLE_APP.get('IMG_SAVE_DIR').exists():
                settings.ARTICLE_APP.get('IMG_SAVE_DIR').mkdir(parents=True)
            with open(img_path, 'wb') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            res = {'name': img.name, 'url': f'/static/article_app/img/{img_name}', 'title': name}
        else:
            logger.info('img upload valid fail: %s', form.errors)
            res = 2000
        return Response(res)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-last_edit_time', '-create_time')
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', 'content')  # 搜索字段
    ordering_fields = ('last_edit_time', 'create_date',)
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]  # 默认使用 jwt 认证
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        # list 和 retrieve 不进行权限校验
        if self.action in ('list', 'retrieve'):
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        # 列表和详情页使用不同的 serializer，返回不同的字段
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    def get_queryset(self):
        # 管理员显示所有的文章，登录用户显示自己和状态为公开的，非登录只显示状态为公开的
        user = self.request.user
        if user and user.is_authenticated:
            if user.is_superuser:
                return self.queryset
            else:
                return self.queryset.filter(Q(status=ArticleStatus.display.value) | Q(author=user))
        else:
            return self.queryset.filter(status=ArticleStatus.display.value)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            # 同一 IP 不重复增加浏览量，作者自己不增加浏览量
            if (ArticleActivityLog.objects.filter(article=instance, user_ip=request.META['CLIENT_IP']).first() is None
                    and instance.author != request.user):
                instance.view_count += 1
            # 记录浏览记录
            viewer = request.user if not request.user.is_anonymous else None
            active_log = ArticleActivityLog.objects.create(article=instance, user=viewer,
                                                           user_ip=request.META['CLIENT_IP'],
                                                           action_type=ArticleActionType.view.value)
            active_log.save()
            instance.save()
            return Response(serializer.data)
        except Http404:
            return Response(2001)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user or request.user.is_superuser:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            if not instance.author and request.user.is_superuser:
                serializer.validated_data['author'] = request.user
            self.perform_update(serializer)
            # 记录更新操作
            edit_log = ArticleEditLog.objects.create(article=instance, edit_user=request.user)
            edit_log.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response(1000)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.is_superuser or instance.author == request.user:
                self.perform_destroy(instance)
                return Response(0)
            else:
                return Response(1000)
        except Http404:
            return Response(2001)


class ArticleFileView(APIView):
    """
    直接上传文章（Markdown 文件）
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]  # 需要管理员权限

    def post(self, request):
        article_file = request.FILES.get('article_file')
        if article_file:
            suffix = article_file.name.rsplit('.', 1)[-1]
            if suffix == 'md':
                if article_file.size <= settings.ARTICLE_APP.get('MD_FILE_MAX_SIZE'):
                    title = article_file.name.rsplit('.', 1)[0]
                    content = article_file.read().decode('utf-8')
                    # 保存文件
                    article_path = save_article_file(title, content, settings.ARTICLE_APP.get('MD_FILE_SAVE_DIR'))
                    # 添加数据库记录
                    article_info = {
                        'title': title,
                        'abstract': generate_article(content),
                        'content': content,
                        'file_path': article_path,
                        'author': request.user,
                    }
                    Article.objects.create(**article_info).save()
                    res = 0
                else:
                    res = 2003
            else:
                res = 2002
        else:
            res = 2002
        return Response(res)
