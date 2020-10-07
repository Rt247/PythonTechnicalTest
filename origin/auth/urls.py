"""
    URL path for generating authentication tokens
        GET request with username and password parameters
"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token', obtain_auth_token, name='auth-token'),
]