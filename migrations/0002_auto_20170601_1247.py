# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_paranoiabot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='custom_player_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
