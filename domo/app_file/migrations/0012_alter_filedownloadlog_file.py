# Generated by Django 4.2.11 on 2024-08-26 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_file', '0011_alter_filedownloadlog_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedownloadlog',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_file.file', verbose_name='文件'),
        ),
    ]
