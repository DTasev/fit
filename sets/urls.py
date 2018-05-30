from django.urls import path

from sets.views import repeat_set, UpdateSet, view_readonly_set, AddSetView, DeleteSet

app_name = 'sets'

# the pk here will refer to an exercise object, not a set object
urlpatterns = [
    path('<int:pk>', AddSetView.as_view(), name="add"),
    path('delete/<int:pk>', DeleteSet.as_view(), name="delete"),
    path('repeat/<int:pk>', repeat_set, name="repeat"),
    path('update/<int:pk>', UpdateSet.as_view(), name="update"),
    path('readonly/<int:pk>', view_readonly_set, name="view_readonly"),
]
