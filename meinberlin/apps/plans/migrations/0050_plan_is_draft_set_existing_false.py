# Generated by Django 2.2.24 on 2021-08-27 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0049_plan_contact_fields_help_texts"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="is_draft",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
