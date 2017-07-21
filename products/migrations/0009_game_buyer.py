# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 01:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0008_game_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_buyer', to=settings.AUTH_USER_MODEL),
        ),
    ]
