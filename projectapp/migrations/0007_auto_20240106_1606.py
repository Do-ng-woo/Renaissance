# Generated by Django 3.2.23 on 2024-01-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0006_auto_20240106_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
