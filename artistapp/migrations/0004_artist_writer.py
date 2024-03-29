# Generated by Django 3.2.23 on 2024-01-07 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artistapp', '0003_alter_artist_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artist', to=settings.AUTH_USER_MODEL),
        ),
    ]
