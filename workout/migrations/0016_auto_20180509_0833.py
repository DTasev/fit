# Generated by Django 2.0.3 on 2018-05-09 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0015_auto_20180508_2234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ['id']},
        ),
    ]
