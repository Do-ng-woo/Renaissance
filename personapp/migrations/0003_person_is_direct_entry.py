# Generated by Django 3.2.23 on 2024-01-25 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personapp', '0002_person_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_direct_entry',
            field=models.BooleanField(default=False),
        ),
    ]
