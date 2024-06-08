# Generated by Django 5.0.6 on 2024-06-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_studentregistration_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('deadline_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]