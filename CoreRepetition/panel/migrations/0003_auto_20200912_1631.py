# Generated by Django 3.1.1 on 2020-09-12 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_auto_20200912_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='panel.course'),
        ),
    ]
