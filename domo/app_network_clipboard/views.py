from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_network_clipboard.models import Clipboard
from app_network_clipboard.serializers import ClipboardSerializer
from constants.constants import ClipboardPrivacy
from constants.reponse_codes import ResponseCode


class ClipboardViewSet(ModelViewSet):
    queryset = Clipboard.objects.all()
    serializer_class = ClipboardSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_time', 'name']
    ordering = ['-created_time']
    authentication_classes = [JWTAuthentication]
    permission_classes = []

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
        # 添加创建用户信息
        if request.user and request.user.is_authenticated:
            serializer.validated_data['created_user'] = request.user
        else:
            serializer.validated_data['created_user'] = None
            if serializer.validated_data['privacy_type'] != ClipboardPrivacy.shared_no_pass.value:
                return Response(ResponseCode.ONLY_SHARED)
        if privacy_type == ClipboardPrivacy.shared_pass.value:
            if password is None or not password.strip():
                return Response(ResponseCode.SHARED_PASSWORD_EMPTY)
            if len(password) < 6:
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
