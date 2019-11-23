# Generated by Django 2.2.1 on 2019-10-07 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0005_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=32)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='img')),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=4, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('user_type', models.IntegerField(default=1)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
