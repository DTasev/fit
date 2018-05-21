from django.urls import path

from sets.views import add_set, del_set, repeat_set, EditSet, view_readonly_set, AddSetView

app_name = 'sets'

# the pk here will refer to an exercise object, not a set object
urlpatterns = [
    path('<int:pk>', AddSetView.as_view(), name="add_set"),
    path('delete/<int:pk>', del_set, name="del_set"),
    path('repeat/<int:pk>', repeat_set, name="repeat_set"),
    path('edit/<int:pk>', EditSet.as_view(), name="edit_set"),
    path('readonly/<int:pk>', view_readonly_set, name="view_readonly"),
]
