# Generated by Django 2.0.3 on 2018-05-04 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0007_auto_20180504_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='primary_muscle_group',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='workout',
            name='secondary1_muscle_group',
            field=models.CharField(max_length=50),
        ),
    ]
