# Generated by Django 3.1.1 on 2020-09-12 12:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
