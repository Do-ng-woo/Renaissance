# Generated by Django 3.2.23 on 2024-01-25 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personapp', '0003_person_is_direct_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_direct_entry',
        ),
    ]
