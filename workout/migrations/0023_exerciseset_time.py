# Generated by Django 2.0.3 on 2018-05-30 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0022_auto_20180527_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseset',
            name='time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
