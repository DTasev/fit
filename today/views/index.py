import datetime

from django.urls import reverse_lazy
from django.utils.timezone import now
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        month_parmeter = self.request.GET.get('month', None)
        if not month_parmeter:
            month_parmeter = now().strftime("%Y-%m")
        context["selected_month"] = month_parmeter
        return context

    def get_queryset(self):
        # check if page present
        month_parameter = self.request.GET.get("month", None)
        if not month_parameter:
            # assume all months have 30 days because dealing with days and months is a pain
            today = datetime.date.today()
            return Workout.objects.filter(user_id=self.request.user,
                                          date__month=today.month,
                                          date__year=today.year)
        else:
            return Workout.objects.filter(user_id=self.request.user,
                                          date__year=month_parameter[0:4],
                                          date__month=month_parameter[5:])

        # if not then get when date <= today - 1 week
        # else if present then get when date <= today - 1 + (page) weeks


class ShareView(generic.DetailView):
    model = Workout
    template_name = 'today/share.html'


class DeleteView(generic.DeleteView):
    model = Workout
    success_url = reverse_lazy('today:history')
