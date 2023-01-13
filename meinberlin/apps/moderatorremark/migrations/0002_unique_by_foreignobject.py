# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-28 14:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("meinberlin_moderatorremark", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="moderatorremark",
            unique_together=set([("item_content_type", "item_object_id")]),
        ),
    ]
