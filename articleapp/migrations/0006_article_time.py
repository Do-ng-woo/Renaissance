# Generated by Django 3.2.23 on 2023-11-22 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articleapp', '0005_article_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
