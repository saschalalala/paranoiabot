# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_paranoiabot', '0004_auto_20170601_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='channel_id',
            field=models.IntegerField(max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='telegram_id',
            field=models.PositiveIntegerField(),
        ),
    ]
