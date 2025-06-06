from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_network_clipboard.models import Clipboard
from app_network_clipboard.serializers import ClipboardSerializer, ClipboardListSerializer
from constants.constants import ClipboardPrivacy
from constants.reponse_codes import ResponseCode


class ClipboardViewSet(ModelViewSet):
    queryset = Clipboard.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_time', 'name']
    ordering = ['-created_time']
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get_serializer_class(self):
        # 列表和详情页使用不同的 serializer，返回不同的字段
        if self.action == 'list':
            return ClipboardListSerializer
        return ClipboardSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user  # type: User
        if user and user.is_authenticated:
            if not user.is_superuser:
                queryset = queryset.filter(Q(created_user=None) | Q(created_user=user))
        else:
            queryset = queryset.filter(created_user=None)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_accessible_by_user(request.user):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(ResponseCode.PERMISSION_DENIED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        privacy_type = serializer.validated_data['privacy_type']
        password = serializer.validated_data.get('password')
        if privacy_type not in ClipboardPrivacy.values():
            return Response(ResponseCode.PARAM_ERROR)
        # 添加创建用户信息
        if request.user and request.user.is_authenticated:
            serializer.validated_data['created_user'] = request.user
        else:
            if serializer.validated_data['privacy_type'] == ClipboardPrivacy.private.value:
                return Response(ResponseCode.ONLY_SHARED)
            serializer.validated_data['created_user'] = None
        if privacy_type == ClipboardPrivacy.shared_pass.value:
            if password is None or not password.strip():
                return Response(ResponseCode.SHARED_PASSWORD_EMPTY)
            if len(password) < 4:
                return Response(ResponseCode.SHARED_PASSWORD_ERROR)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        created_user = serializer.validated_data.get('created_user')
        privacy_type = serializer.validated_data.get('privacy_type')
        password = serializer.validated_data.get('password')
        if created_user and created_user != request.user:
            return Response(ResponseCode.PERMISSION_DENIED)
        if privacy_type == ClipboardPrivacy.shared_pass.value:
            if password is None or not password.strip():
                return Response(ResponseCode.SHARED_PASSWORD_EMPTY)
            if len(password) < 6:
                return Response(ResponseCode.SHARED_PASSWORD_ERROR)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
