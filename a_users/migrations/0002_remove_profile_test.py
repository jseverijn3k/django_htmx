# Generated by Django 5.0 on 2024-01-04 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='test',
        ),
    ]
