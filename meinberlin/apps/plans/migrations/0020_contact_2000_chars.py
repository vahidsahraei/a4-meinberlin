# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 15:09
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0019_point_label_helptext"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="contact",
            field=models.TextField(max_length=1000, verbose_name="Contact"),
        ),
    ]
