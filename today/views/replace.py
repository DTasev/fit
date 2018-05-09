import datetime
import random

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from workout.models import WorkoutExercise, Exercise


class ReplaceExercise(SingleObjectMixin, View):
    model = WorkoutExercise

    def post(self, request, *args, **kwargs):
        e = self.get_object()

        new_exercise = random.sample(list(Exercise.objects.filter(muscle_group=e.exercise.muscle_group)), k=1)[0]

        e.exercise = new_exercise
        e.save()
        return redirect(reverse('today:index'))
