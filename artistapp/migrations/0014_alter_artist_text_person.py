# Generated by Django 3.2.23 on 2024-01-26 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistapp', '0013_alter_artist_text_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='text_person',
            field=models.JSONField(default=list),
        ),
    ]
