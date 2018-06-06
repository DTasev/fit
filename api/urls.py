from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.views import WorkoutViewSet, AddNewSet

app_name = 'api'


class DocsView(APIView):
    """
    RESTFul Documentation of my app
    """

    def get(self, request, *args, **kwargs):
        apidocs = {
            'auth-login-token': request.build_absolute_uri('auth-login-token/'),
            'today': request.build_absolute_uri('today/'),
            "sets/add/":request.build_absolute_uri('sets/add/')
        }
        return Response(apidocs)


urlpatterns = [
    path('', DocsView.as_view()),
    path('auth-login-token/', obtain_auth_token, name="auth-login-token"),
    path('today/', WorkoutViewSet.as_view({'get': 'retrieve'}), name="today"),
    path('sets/add/', AddNewSet.as_view({'post': 'create'}), name="sets-add"),
]
