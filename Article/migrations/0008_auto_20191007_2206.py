# Generated by Django 2.2.1 on 2019-10-07 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0007_auto_20191007_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='click',
        ),
        migrations.RemoveField(
            model_name='article',
            name='recommend',
        ),
    ]
