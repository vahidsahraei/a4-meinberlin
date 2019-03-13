# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_documents', '0006_update_weight_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
