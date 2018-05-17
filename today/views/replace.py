import datetime
import random

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from workout.models import WorkoutExercise, Exercise
from django.contrib import messages


class ReplaceExercise(SingleObjectMixin, View):
    model = WorkoutExercise

    def post(self, request, *args, **kwargs):
        e = self.get_object()
        if e.sets.count() == 0:
            new_exercise = random.sample(list(Exercise.objects.filter(muscle_group=e.exercise.muscle_group)), k=1)[0]

            e.exercise = new_exercise
            e.save()
        else:
            # send forward the message to be read in the index view after the redirect
            messages.add_message(request, messages.ERROR, 'Cannot replace an exercise that has existing sets.')
        return redirect(reverse('today:index'))
