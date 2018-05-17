import datetime

from django.urls import reverse_lazy
from django.views import generic

from workout.models import Workout
from django.contrib import messages


class IndexView(generic.ListView):
    model = Workout
    template_name = 'today/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        storage = messages.get_messages(self.request)
        msg = None
        for message in storage:
            msg = message
        if msg:
            context["sets_error_message"] = msg
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Workout.objects.filter(user_id=self.request.user, date=datetime.date.today()).first()


class HistoryView(generic.ListView):
    model = Workout
    template_name = 'today/history.html'

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user)


class DeleteView(generic.DeleteView):
    model = Workout
    success_url = reverse_lazy('today:history')
