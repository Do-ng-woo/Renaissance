# Generated by Django 3.2.23 on 2024-01-03 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artistapp', '0002_alter_artist_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['title']},
        ),
    ]
