from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from workout.models import Workout, WorkoutDataCache


class CompleteWorkout(generic.DetailView):
    model = Workout

    def post(self, request, *args, **kwargs):
        w = self.get_object()
        data_cache, created = WorkoutDataCache.objects.get_or_create(workout=w)

        if not w.completed:
            w.completed = True
            if w.start_time:
                w.end_time = timezone.now()

            data_cache.compute_kcals(w, request.user)
        else:
            w.completed = False
            w.start_time = None
            w.end_time = None
            data_cache.delete()
        w.save()
        return redirect(reverse('today:index'))
