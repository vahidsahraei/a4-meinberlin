# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 11:48
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_topicprio", "0008_topic_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="labels",
            field=models.ManyToManyField(
                related_name="meinberlin_topicprio_topic_label",
                to="a4labels.Label",
                verbose_name="Labels",
            ),
        ),
    ]
