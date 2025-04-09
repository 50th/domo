from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_network_clipboard.models import Clipboard
from app_network_clipboard.serializers import ClipboardSerializer
from constants.reponse_codes import ResponseCode


class ClipboardViewSet(ModelViewSet):
    queryset = Clipboard.objects.all()
    serializer_class = ClipboardSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_time', 'name']
    ordering = ['-created_time']
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user and request.user.is_authenticated:
            serializer.validated_data['created_user'] = request.user
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
            return Response(ResponseCode.PERMISSION_DENIED)
