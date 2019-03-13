# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-06 09:03
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('meinberlin_cms', '0026_update_wagtail'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpPages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_page', models.ForeignKey(blank=True, help_text='Please add a link to the help page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='help_page', to='wagtailcore.Page', verbose_name='Help Page')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
