from django.urls import path

from app_system import views

urlpatterns = [
    path('sys-info/', views.SystemView.as_view(), name='sys-info'),
]
