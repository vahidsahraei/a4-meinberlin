# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-25 20:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_plans', '0031_update_choices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='topic',
            new_name='topics',
        ),
    ]
