# Generated by Django 5.0.2 on 2024-02-22 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0006_calendarevent_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendarevent',
            name='date',
        ),
    ]
