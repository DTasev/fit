from django.urls import path

from sets.views import add_set, del_set, repeat_set, UpdateSet, view_readonly_set, AddSetView

app_name = 'sets'

# the pk here will refer to an exercise object, not a set object
urlpatterns = [
    path('<int:pk>', AddSetView.as_view(), name="add"),
    path('delete/<int:pk>', del_set, name="del"),
    path('repeat/<int:pk>', repeat_set, name="repeat"),
    path('update/<int:pk>', UpdateSet.as_view(), name="update"),
    path('readonly/<int:pk>', view_readonly_set, name="view_readonly"),
]
