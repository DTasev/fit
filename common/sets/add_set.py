from django.contrib.auth.models import User
from django.utils import timezone

from common.sets.add_set_data import AddSetData
from workout.models import WorkoutExercise, ExerciseSet


def add_set_routine(obj: WorkoutExercise, data: AddSetData) -> ExerciseSet:
    workout = obj.workout
    if not workout.start_time:
        workout.start_time = timezone.now()
        workout.save()
    latest_set = obj.sets.create(kgs=data.kgs, reps=data.reps, time=timezone.now())
    return latest_set


def get_last_exercise(workout_exercise: WorkoutExercise, user: User) -> WorkoutExercise:
    past_exercises = WorkoutExercise.objects.filter(workout__user=user,
                                                    exercise__name=workout_exercise.exercise.name)
    exercise_from_last_time = None
    if len(past_exercises) > 1:
        # get the data for the last time the exercise was performed
        past_exercises = past_exercises[len(past_exercises) - 2]
        if past_exercises.sets.count() != 0:
            exercise_from_last_time = past_exercises
    return exercise_from_last_time
