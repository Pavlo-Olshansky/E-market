# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 14:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20170718_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['publication_date']},
        ),
    ]