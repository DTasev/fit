from django.urls import path

from sets.views import add_set, del_set, repeat_set, EditSet

app_name = 'sets'

urlpatterns = [
    path('<int:pk>', add_set, name="add_set"),
    path('delete/<int:pk>', del_set, name="del_set"),
    path('repeat/<int:pk>', repeat_set, name="repeat_set"),
    path('edit/<int:pk>', EditSet.as_view(), name="edit_set"),
]
