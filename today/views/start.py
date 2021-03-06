from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from workout.models import Workout


class StartWorkout(SingleObjectMixin, View):
    model = Workout

    def post(self, request, *args, **kwargs):
        w = self.get_object()
        w.start_time = timezone.now()
        w.save()
        return redirect(reverse('today:index'))
