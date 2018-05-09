import datetime

from django.urls import reverse_lazy
from django.views import generic

from workout.models import Workout


class IndexView(generic.ListView):
    model = Workout
    template_name = 'today/index.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Workout.objects.get(user_id=self.request.user, date=datetime.date.today())


class HistoryView(generic.ListView):
    model = Workout
    template_name = 'today/history.html'

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user)


class DeleteView(generic.DeleteView):
    model = Workout
    success_url = reverse_lazy('today:history')
