import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

class UserAccountTestCase(APITestCase):
    """
        Testing the workflows for user account creation
    """

    def setUp(self):
        """
            Setup an user account with correct token
        """
        self.user = User.objects.create_user(username="existing_user",
                                            password="super_strong_password")
        self.token = Token.objects.create(user=self.user)


    def api_authentication(self):
        """
            Authenitcate a user with a authorizsation token
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_sign_up_redirect(self):
        """
            Test successful sign up which leads to a redirect
        """
        data = {"username": "test", "password1": "super_strong_password",
                "password2": "super_strong_password"}

        response = self.client.post("/accounts/signup/", data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_sign_up_fail(self):
        """
            Test fail sign up which returns a 200 status status_code
            and visual error messaage on interface
        """
        data = {"username": "test", "password1": "super_strong_password",
                "password2": "wrong_password"}

        response = self.client.post("/accounts/signup/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_redirect(self):
        """
            Test successful login which leads to a redirect
        """
        self.api_authentication()
        data = {"username": "existing_user", "password": "super_strong_password"}

        response = self.client.post("/accounts/login/", data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_login_wrong_password(self):
        """
            Test fail login up with wrong password which returns a
            200 status status_code and visual error messaage on interface
        """
        self.api_authentication()
        data = {"username": "existing_user", "password": "wrong_password"}

        response = self.client.post("/accounts/login/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_username(self):
        """
            Test fail login up with wrong username which returns a 200
            status status_code and visual error messaage on interface
        """
        self.api_authentication()
        data = {"username": "unknown_user", "password": "super_strong_password"}

        response = self.client.post("/accounts/login/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
