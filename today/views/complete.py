from django.shortcuts import redirect
from django.urls import reverse

from workout.models import Workout


def complete_workout(request, pk):
    if request.method == "POST":
        w = Workout.objects.get(id=pk)
        w.completed = not w.completed
        w.save()
        return redirect(reverse('today:index'))
