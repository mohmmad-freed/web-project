# Generated by Django 5.0.6 on 2024-06-03 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='completed_courses',
            field=models.ManyToManyField(blank=True, related_name='completed_students', to='studentsapp.course'),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='room_no',
            field=models.CharField(default='4', max_length=10),
        ),
    ]
