# Generated by Django 3.2.23 on 2024-01-24 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0009_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='description',
            old_name='artist',
            new_name='project',
        ),
    ]
