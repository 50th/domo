from typing import Dict, Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录成功后返回的数据
    """
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        # 在返回数据中增加 user_id 和用户名
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['is_superuser'] = self.user.is_superuser
        return data
