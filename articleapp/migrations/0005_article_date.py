# Generated by Django 3.2.23 on 2023-11-22 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articleapp', '0004_article_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
