# Generated by Django 3.2.23 on 2024-01-10 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistapp', '0005_artist_hide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='hide',
            field=models.BooleanField(default=True),
        ),
    ]
