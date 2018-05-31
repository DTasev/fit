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

            # this is a special button that uses the time from the latest set
            if w.start_time:
                if request.POST.get("complete-with-latest-set", None):
                    latest_set_time_available = getattr(w.workoutexercise_set.last().sets.last(), "time", None)
                else:
                    latest_set_time_available = None

                if latest_set_time_available:
                    w.end_time = latest_set_time_available
                else:
                    w.end_time = timezone.now()

            data_cache.compute_kcals(w, request.user)
        else:
            w.completed = False
            w.start_time = None
            w.end_time = None
            data_cache.delete()
        w.save()
        return redirect(reverse('today:index'))
