from django.urls import path

from today.views.create import create_workout
from today.views.index import IndexView, HistoryView
from today.views.complete import complete_workout
from today.views.sets import add_set, del_set

app_name = 'today'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create', create_workout, name="create"),
    path('complete/<int:pk>', complete_workout, name="complete"),
    path('history', HistoryView.as_view(), name="history"),
    path('sets/<int:pk>', add_set, name="add_set"),
    path('sets/delete/<int:pk>', del_set, name="del_set"),

]
