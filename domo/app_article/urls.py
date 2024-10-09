from django.urls import path, include
from rest_framework import routers

from app_article import views

router = routers.DefaultRouter()  # 如果需要不在 url 末尾添加加 /，可以传入参数 trailing_slash=False
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('view-count-top/', views.ArticleViewCountView.as_view()),
    path('article-img/', views.ArticleImgView.as_view()),
    path('article-file/', views.ArticleFileView.as_view()),
]
