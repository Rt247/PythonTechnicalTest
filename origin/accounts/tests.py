import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

class UserSignUp(APITestCase):

    def test_sign_up_redirect(self):
        data = {"username": "test", "password1": "super_strong_password",
                "password2": "super_strong_password"}

        response = self.client.post("/accounts/signup/", data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_sign_up_fail(self):
        data = {"username": "test", "password1": "super_strong_password",
                "password2": "super_password"}

        response = self.client.post("/accounts/signup/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
