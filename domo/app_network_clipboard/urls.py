from django.urls import path, include
from rest_framework import routers

from app_network_clipboard import views

router = routers.DefaultRouter()
router.register('clipboards', views.ClipboardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
