# Generated by Django 3.2.23 on 2023-11-23 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articleapp', '0008_article_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
