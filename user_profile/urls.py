from django.urls import path

from .views import ProfileDetail

app_name = 'user_profile'

urlpatterns = [
    path('<username>', ProfileDetail.as_view(), name='index'),
]
