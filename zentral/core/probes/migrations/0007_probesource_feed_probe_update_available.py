# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('probes', '0006_auto_20161209_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='probesource',
            name='feed_probe_update_available',
            field=models.BooleanField(default=False),
        ),
    ]
