# Generated by Django 2.0.3 on 2018-05-03 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0004_auto_20180503_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='exercises',
        ),
    ]
