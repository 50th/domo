from django.urls import path, include
from rest_framework import routers

from app_video import views

router = routers.DefaultRouter()
router.register(r'videos', views.VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('video_serve/<str:video_uuid>/', views.video_serve),
]
