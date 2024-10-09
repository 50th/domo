from pathlib import Path

from django.conf import settings
from django import forms
from rest_framework import serializers

from app_article.models import Article
from constants.constants import ArticleActionType
from utils.common_funcs import generate_article, save_article_file


class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username', default='')
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    last_edit_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'abstract', 'status', 'author', 'author_name', 'create_time', 'last_edit_time',
                  'view_count', 'like_count']
        read_only_fields = ['id', 'author', 'create_time']


class ArticleSerializer(ArticleListSerializer):
    status_display = serializers.ReadOnlyField(source='get_status_display')

    def create(self, validated_data):
        content = validated_data['content']
        abstract = generate_article(content)
        file_path = save_article_file(validated_data['title'], content, settings.ARTICLE_APP.get('MD_FILE_SAVE_DIR'))
        return Article.objects.create(abstract=abstract, file_path=file_path, **validated_data)

    def update(self, instance, validated_data):
        content = validated_data.get('content')
        instance.abstract = generate_article(content)
        if instance.file_path:
            instance.file_path = Path(instance.file_path)
            if instance.file_path.exists():
                instance.file_path.unlink()
        instance.file_path = save_article_file(validated_data['title'], content,
                                               settings.ARTICLE_APP.get('MD_FILE_SAVE_DIR'))
        return super().update(instance, validated_data)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'status', 'status_display', 'author', 'author_name', 'create_time',
                  'last_edit_time', 'view_count', 'like_count']


class UploadImgForm(forms.Form):
    img = forms.ImageField()

    def clean_img(self):
        img = self.cleaned_data['img']
        if img.size > settings.ARTICLE_APP.get('MAX_IMAGE_SIZE', 1024 * 1024 * 10):
            raise forms.ValidationError('图片过大')
        return img
