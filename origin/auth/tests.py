import json
import sys

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from bonds.models import Bond

validPostBondData = {
    "isin": "FR0000131104",
    "size": 1000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}

validGetBondData = {
    "isin": "FR0000131104",
    "size": 1000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83",
    "legal_name": "BNP PARIBAS"
}

validGetBondDataTwo = {
    "isin": "GR0000131104",
    "size": 1000000,
    "currency": "GBR",
    "maturity": "2020-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83",
    "legal_name": "BNP PARIBAS"
}

class BondViewListAuthTestCase(APITestCase):
    """
        Test case to validate authentication is enforced for user
        access to bonds
    """

    bond_url = reverse("bonds")

    def setUp(self):
        """
            Setup the two different users and bonds for each user
            Generate tokens for each user
        """
        self.user = User.objects.create_user(username="test",
                                            password="super_strong_password")
        self.token = Token.objects.create(user=self.user)

        self.user_empty = User.objects.create_user(username="empty",
                                             password="super_strong_password")
        self.user_empty_token = Token.objects.create(user=self.user_empty)

        self.bond_one = Bond(user=self.user, **validGetBondData)
        self.bond_one.save()

        self.bond_two = Bond(user=self.user_empty, **validGetBondDataTwo)
        self.bond_two.save()

    def api_authentication(self, token):
        """
            Authenticate the client with a given token
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_user_get_authenticated(self):
        """
            Validate bond access for valid tokens for a user
        """
        self.api_authentication(self.token)

        response = self.client.get(self.bond_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_unauthenticated(self):
        """
            Validate bond access restricted to invalid tokens for a user
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.bond_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_post_authenticated(self):
        """
            Validate bond post for valid tokens for a user
        """
        self.api_authentication(self.token)
        response = self.client.post(self.bond_url,
                                    data=json.dumps(validPostBondData),
                                    content_type='raw')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_post_unauthenticated(self):
        """
            Validate bond post restricted for invalid tokens for a user
        """
        self.client.force_authenticate(user=None)
        response = self.client.post(self.bond_url,
                                    data=json.dumps(validPostBondData),
                                    content_type='raw')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_bonds_only_retrieve(self):
        """
            Test data partition at a user level for bonds for query tokens
        """
        self.api_authentication(self.token)
        response = self.client.get(self.bond_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0], validGetBondData)
        self.assertEqual(len(json.loads(response.content)), 1)

        self.api_authentication(self.user_empty_token)
        response_empty_user = self.client.get(self.bond_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response_empty_user.content)[0], validGetBondDataTwo)
        self.assertEqual(len(json.loads(response_empty_user.content)), 1)

