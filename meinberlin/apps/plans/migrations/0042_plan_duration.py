# Generated by Django 2.2.17 on 2021-02-04 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0041_add_image_copyright_rm_required"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="duration",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Duration"
            ),
        ),
    ]
