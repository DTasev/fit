import datetime

from django.shortcuts import redirect
from django.urls import reverse

from workout.models import Workout


def complete_workout(request, pk):
    if request.method == "POST":
        w = Workout.objects.get(id=pk)
        if not w.completed:
            w.completed = True
            if not w.start_time:
                w.start_time = datetime.datetime.now()
            w.end_time = datetime.datetime.now()
        else:
            w.completed = False
            w.start_time = None
            w.end_time = None

        w.save()
        return redirect(reverse('today:index'))
