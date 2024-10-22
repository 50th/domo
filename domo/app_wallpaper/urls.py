from django.urls import path, include
from rest_framework import routers

from app_wallpaper import views

router = routers.DefaultRouter()
router.register(r'wallpapers', views.WallpaperViewSet)

urlpatterns = [
    path('upload-wallpaper/', views.upload_wallpaper),
    path('', include(router.urls)),
]
