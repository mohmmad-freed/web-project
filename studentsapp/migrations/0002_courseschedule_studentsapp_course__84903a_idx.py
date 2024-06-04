# Generated by Django 5.0.6 on 2024-06-03 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='courseschedule',
            index=models.Index(fields=['course', 'days', 'start_time', 'end_time'], name='studentsapp_course__84903a_idx'),
        ),
    ]