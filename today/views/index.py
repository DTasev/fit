import datetime

from django.views import generic

from workout.models import Workout


class IndexView(generic.ListView):
    model = Workout
    template_name = 'today/index.html'

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user, date=datetime.date.today()).first()


class HistoryView(generic.ListView):
    model = Workout
    template_name = 'today/history.html'

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user)
