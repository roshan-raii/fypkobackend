# Generated by Django 5.0.4 on 2024-04-06 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moduleyear',
            old_name='module_id',
            new_name='module',
        ),
    ]
