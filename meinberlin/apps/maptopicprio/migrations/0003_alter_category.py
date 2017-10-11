# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 15:37
from __future__ import unicode_literals

import adhocracy4.categories.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_maptopicprio', '0002_name_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maptopic',
            name='category',
            field=adhocracy4.categories.fields.CategoryField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='a4categories.Category'),
        ),
    ]
