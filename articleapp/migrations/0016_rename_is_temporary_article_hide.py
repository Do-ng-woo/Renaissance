# Generated by Django 3.2.23 on 2024-01-10 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articleapp', '0015_article_is_temporary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='is_temporary',
            new_name='hide',
        ),
    ]
