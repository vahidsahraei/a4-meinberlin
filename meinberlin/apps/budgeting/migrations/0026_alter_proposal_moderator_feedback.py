# Generated by Django 3.2.16 on 2022-10-21 13:03

from django.db import migrations
import meinberlin.apps.moderatorfeedback.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0025_alter_proposal_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='moderator_feedback',
            field=meinberlin.apps.moderatorfeedback.fields.ModeratorFeedbackField(blank=True, choices=[('CONSIDERATION', 'Under consideration'), ('CHECKED', 'Checked'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted')], default=None, help_text='The editing status appears below the title of the idea in red, yellow or green. The idea provider receives a notification.', max_length=254, null=True, verbose_name='Processing status'),
        ),
    ]
