# Generated by Django 2.0.3 on 2018-05-08 21:13

from django.db import migrations, models
import django.db.models.deletion


def split_old_sets(apps, schema_editor):
    WorkoutExercise = apps.get_model('workout', 'WorkoutExercise')
    ExerciseSet = apps.get_model('workout', 'ExerciseSet')

    for w in WorkoutExercise.objects.all():
        if w.old_sets != "":
            for set in w.old_sets.split("|"):
                # this gives back a list [<kgs>, <reps>]
                kgs_and_reps = set.split("x")
                ExerciseSet.objects.create(workout_exercise=w, kgs=float(kgs_and_reps[0]), reps=float(kgs_and_reps[1]))


class Migration(migrations.Migration):
    dependencies = [
        ('workout', '0013_auto_20180504_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.IntegerField()),
                ('kgs', models.FloatField()),
            ],
        ),
        migrations.RenameField(
            model_name='workoutexercise',
            old_name='sets',
            new_name='old_sets',
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='workout_exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets',
                                    to='workout.WorkoutExercise'),
        ),
        migrations.RunPython(split_old_sets, lambda x, y: x),
    ]
