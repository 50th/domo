# Generated by Django 4.2.11 on 2024-06-13 07:01

import app_file.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_file', '0006_alter_file_file_path_alter_file_upload_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_path',
            field=models.FileField(null=True, upload_to=app_file.models.create_file_path, verbose_name='文件'),
        ),
    ]
