from django.contrib.auth.models import User
from django.db import models

from constants.constants import ArticleStatus, ArticleActionType


class Article(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False, verbose_name='文章标题')
    abstract = models.CharField(max_length=256, blank=False, null=False, verbose_name='内容摘要')
    content = models.TextField(blank=False, null=False, verbose_name='文章内容')
    file_path = models.CharField(max_length=128, blank=True, null=False, verbose_name='文章路径')
    status = models.SmallIntegerField(choices=ArticleStatus.to_choices(), default=ArticleStatus.display.value,
                                      verbose_name='文章状态')
    author = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, verbose_name='作者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_edit_time = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')
    view_count = models.IntegerField(default=0, verbose_name='浏览量')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'


class ArticleEditLog(models.Model):
    """
    编辑记录
    """
    article = models.ForeignKey(Article, null=True, on_delete=models.SET_NULL, verbose_name='文章')
    edit_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='用户')
    edit_time = models.DateTimeField(auto_now_add=True, verbose_name='编辑时间')

    class Meta:
        db_table = 'article_edit_log'


class ArticleActivityLog(models.Model):
    article = models.ForeignKey(Article, null=True, on_delete=models.SET_NULL, verbose_name='文章')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='用户')
    user_ip = models.CharField(max_length=128, verbose_name='用户 IP')
    action_type = models.SmallIntegerField(choices=ArticleActionType.to_choices(), default=ArticleActionType.view.value,
                                           verbose_name='动作类型')
    log_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    def __str__(self):
        return f'{self.article.title}_{self.user.username}_{self.action_type}_{self.log_time}'

    class Meta:
        db_table = 'article_activity_log'
