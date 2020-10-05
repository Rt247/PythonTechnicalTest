from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('token', obtain_auth_token, name='auth-token'),
]