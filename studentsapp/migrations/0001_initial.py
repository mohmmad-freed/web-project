# Generated by Django 5.0.6 on 2024-06-03 18:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('instructor_name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('prerequisites', models.ManyToManyField(blank=True, to='studentsapp.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(choices=[('S,T,T', 'Sunday, Tuesday, Thursday'), ('M,W', 'Monday, Wednesday')], max_length=7)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('room_no', models.CharField(max_length=10)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentsapp.course')),
            ],
            options={
                'unique_together': {('course', 'days', 'start_time', 'end_time', 'room_no')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('schedules', models.ManyToManyField(related_name='students', to='studentsapp.courseschedule')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
