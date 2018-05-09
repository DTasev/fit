import datetime
import random

from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse

from workout.models import Workout, Exercise, WorkoutExercise


def get_exercises(muscle_group):
    if muscle_group == "Chest":
        return muscle_group
    elif muscle_group == "Back":
        return muscle_group
    elif muscle_group == "Arms":
        return muscle_group
    elif muscle_group == "Shoulders":
        return muscle_group
    elif muscle_group == "Legs":
        return muscle_group


def create_workout(request):
    if request.method == "GET":
        return render(template_name="today/create.html", request=request)
    elif request.method == "POST":
        w = find_workout(request)

        w.primary_muscle_group = request.POST["primary"]
        w.secondary_muscle_group = request.POST["secondary"]

        make_exercises(w, w.primary_muscle_group, int(request.POST["primary-count"]))
        make_exercises(w, w.secondary_muscle_group, int(request.POST["secondary-count"]))
        w.save()
        return redirect(reverse('today:index'))


def find_workout(request) -> Workout:
    existing_workout = Workout.objects.filter(user_id=request.user.id, date=datetime.date.today())
    if len(existing_workout) == 0:
        w = Workout.objects.create(user_id=request.user.id, date=datetime.date.today())
    elif len(existing_workout) > 0:
        # wipe all existing workouts for the day
        for w in existing_workout:
            w.delete()
        w = Workout.objects.create(user_id=request.user.id, date=datetime.date.today())
    else:
        w = existing_workout.first()
    return w


def make_exercises(w: Workout, muscle_group: str, count: int):
    relevant_exercises = random.sample(list(Exercise.objects.filter(muscle_group=muscle_group)), k=count)
    with transaction.atomic():
        for e in relevant_exercises:
            WorkoutExercise.objects.create(workout=w, exercise=e)
