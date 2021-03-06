# Generated by Django 2.0.3 on 2018-05-27 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0018_auto_20180526_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutDataCache',
            fields=[
                ('workout', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='data_cache', serialize=False, to='workout.Workout')),
                ('kcals', models.FloatField(verbose_name='KCALs Burned from Workout')),
            ],
        ),
    ]
