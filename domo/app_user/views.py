import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView

from app_user.serializers import CustomTokenObtainPairSerializer
from constants.reponse_codes import ResponseCode

logger = logging.getLogger(__name__)


class UserLoginView(TokenObtainPairView):
    """
    自定义登录成功后返回的数据
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            logger.info('UserLoginView validate fail: %s', e)
            logger.info('UserLoginView request data: %s', request.data)
            return Response(ResponseCode.USERNAME_OR_PASSWORD_ERROR)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
