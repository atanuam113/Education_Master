# Generated by Django 3.2.4 on 2022-03-17 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Edu_Master', '0013_remove_events_event_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='Event_End_Time',
            field=models.TimeField(default='00:00'),
        ),
    ]
