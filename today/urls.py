from django.urls import path, include

from today.views.create import create_workout
from today.views.index import IndexView, HistoryView, DeleteView
from today.views.complete import complete_workout

app_name = 'today'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create', create_workout, name="create"),
    path('complete/<int:pk>', complete_workout, name="complete"),
    path('delete/<int:pk>', DeleteView.as_view(), name="delete"),
    path('history', HistoryView.as_view(), name="history"),
    path('sets/', include('sets.urls'))
]
