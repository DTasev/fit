from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from workout.models import Workout


class CompleteWorkout(generic.DetailView):
    model = Workout

    def post(self, request, *args, **kwargs):
        w = self.get_object()
        if not w.completed:
            w.completed = True
            if w.start_time:
                w.end_time = timezone.now()
        else:
            w.completed = False
            w.start_time = None
            w.end_time = None
        w.save()
        return redirect(reverse('today:index'))
