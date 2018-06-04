from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.views import APIView

app_name = 'api'


class DocsView(APIView):
    """
    RESTFul Documentation of my app
    """

    def get(self, request, *args, **kwargs):
        apidocs = {
            'auth-login-token': request.build_absolute_uri('auth-login-token/'),
        }
        return Response(apidocs)


urlpatterns = [
    path('', DocsView.as_view()),
    path('auth-login-token/', obtain_auth_token, name="auth-login-token"),
]
