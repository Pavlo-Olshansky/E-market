# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 12:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('publication_date', models.DateField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('game_type', models.PositiveSmallIntegerField(choices=[(1, 'Hearthstone'), (2, 'WOW'), (3, 'HOTS')])),
                ('is_accepted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_buyer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['publication_date'],
            },
        ),
        migrations.CreateModel(
            name='LoginPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='login_password_to_game', to='products.Game')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='login_password_of_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos_to_game', to='products.Game')),
            ],
            options={
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.Game'),
        ),
    ]
