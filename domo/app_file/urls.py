from django.urls import path, include
from rest_framework import routers

from app_file import views

router = routers.DefaultRouter()
router.register(r'files', views.FileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('download-count-top/', views.FileDownloadCountView.as_view())
]
