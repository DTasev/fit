from django.shortcuts import redirect
from django.urls import reverse

from workout.models import Workout


def complete_workout(request):
    if request.method == "POST":
        w = Workout.objects.get(id=int(request.POST["workout"]))
        w.completed = not w.completed
        w.save()
        return redirect(reverse('today:index'))
