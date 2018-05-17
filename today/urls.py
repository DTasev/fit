from django.urls import path, include

from today.views.create import create_workout
from today.views.index import IndexView, HistoryView, DeleteView, ShareView
from today.views.complete import complete_workout
from today.views.replace import ReplaceExercise
from today.views.start import StartWorkout

app_name = 'today'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create', create_workout, name="create"),
    path('start/<int:pk>', StartWorkout.as_view(), name="start"),
    path('complete/<int:pk>', complete_workout, name="complete"),
    path('delete/<int:pk>', DeleteView.as_view(), name="delete"),
    path('history', HistoryView.as_view(), name="history"),
    path('share/<int:pk>', ShareView.as_view(), name="share"),
    path('sets/', include('sets.urls')),
    path('replace/<int:pk>', ReplaceExercise.as_view(), name="replace"),
]
