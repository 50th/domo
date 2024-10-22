from rest_framework import serializers

from app_wallpaper.models import Wallpaper


class WallpaperSerializer(serializers.ModelSerializer):
    image_res = serializers.SerializerMethodField(read_only=True)

    def get_image_res(self, obj: Wallpaper):
        return f'{obj.image_width}x{obj.image_height}'

    class Meta:
        model = Wallpaper
        fields = ['id', 'image_name', 'image_size', 'image_res', 'upload_time', 'upload_user']
