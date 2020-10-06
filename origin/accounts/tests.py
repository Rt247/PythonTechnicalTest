import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

class UserAccountTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="existing_user",
                                            password="super_strong_password")
        self.token = Token.objects.create(user=self.user)


    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_sign_up_redirect(self):
        data = {"username": "test", "password1": "super_strong_password",
                "password2": "super_strong_password"}

        response = self.client.post("/accounts/signup/", data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_sign_up_fail(self):
        data = {"username": "test", "password1": "super_strong_password",
                "password2": "wrong_password"}

        response = self.client.post("/accounts/signup/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_redirect(self):
        self.api_authentication()
        data = {"username": "existing_user", "password": "super_strong_password"}

        response = self.client.post("/accounts/login/", data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_login_wrong_password(self):
        self.api_authentication()
        data = {"username": "existing_user", "password": "wrong_password"}

        response = self.client.post("/accounts/login/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_username(self):
        self.api_authentication()
        data = {"username": "unknown_user", "password": "super_strong_password"}

        response = self.client.post("/accounts/login/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
