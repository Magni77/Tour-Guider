# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0004_auto_20170926_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='rate',
        ),
    ]
