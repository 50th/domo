from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from app_user.views import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
