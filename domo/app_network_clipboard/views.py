from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from app_network_clipboard.models import Clipboard
from app_network_clipboard.serializers import ClipboardSerializer


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
        # 添加创建用户信息
        if request.user and request.user.is_authenticated:
            serializer.validated_data['created_user'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
