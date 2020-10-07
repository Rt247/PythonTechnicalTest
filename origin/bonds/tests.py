import json
import sys

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from .models import Bond
from .serializers import BondSerializer
from .thirdpartyapis import get_legal_name
from bonds.views import BondsListView

validPostBondData = {
    "isin": "FR0000131104",
    "size": 1000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}

invalidLeiPostBondData = {
   "isin": "FR0000131104",
   "size": 1000000,
   "currency": "EUR",
   "maturity": "2025-02-28",
   "lei": "invalid"
}

invalidMissingDataPostBondData = {
   "isin": "FR0000131104",
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

validGetBondModData = {
    "isin": "FR0000131104",
    "size": 1000000,
    "currency": "GBP",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83",
    "legal_name": "SNP BARIBAS"
}



class BondViewListRestTestCase(APITestCase):
    """
        Test the GET and POST requests for bonds
    """

    bond_url = reverse("bonds")

    def setUp(self):
        """
            Setup a user and authenticate with token
        """
        self.user = User.objects.create_user(username="test",
                                            password="super_strong_password")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()


    def api_authentication(self):
        """
            Authenticate user with a token header
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_empty_bonds_get(self):
        """
            Test to see if there no user bonds returns an empty list
        """

        response = self.client.get(self.bond_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_user_single_bonds_get(self):
        """
            Test to see if the a singular bond insertion is valid
        """

        bond_one = Bond(**validGetBondData)
        bond_one.save()

        response = self.client.get(self.bond_url)

        Bond.objects.all().delete()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0], validGetBondData)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_user_multiple_bonds_get(self):
        """
            Test to see if multiple bonds inserted are valid
        """

        bond_one = Bond(**validGetBondData)
        bond_one.save()

        bond_two = Bond(**validGetBondModData)
        bond_two.save()

        response = self.client.get(self.bond_url)

        Bond.objects.all().delete()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0], validGetBondData)
        self.assertEqual(json.loads(response.content)[1], validGetBondModData)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_user_bonds_filter_get(self):
        """
            Test to check if the filter works for two parameters
        """
        bond_one = Bond(**validGetBondData)
        bond_one.save()

        bond_two = Bond(**validGetBondModData)
        bond_two.save()

        response = self.client.get(self.bond_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0], validGetBondData)
        self.assertEqual(json.loads(response.content)[1], validGetBondModData)
        self.assertEqual(len(json.loads(response.content)), 2)

        response_filter_legal = self.client.get(self.bond_url,
                                          data={'legal_name': validGetBondData['legal_name']})


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response_filter_legal.content)[0], validGetBondData)
        self.assertEqual(len(json.loads(response_filter_legal.content)), 1)

        response_filter_currency = self.client.get(self.bond_url,
                                                  data={'currency': validGetBondModData['currency']})

        Bond.objects.all().delete()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response_filter_currency.content)[0], validGetBondModData)
        self.assertEqual(len(json.loads(response_filter_currency.content)), 1)

    def test_gleif_legal_name_post(self):
        """
            Test to see if the GLEIF API post missing data fill is correct
            for a known legal name and lei
        """
        response = self.client.post(self.bond_url,
                                    data=json.dumps(validPostBondData),
                                    content_type='raw')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.bond_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0], validGetBondData)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_gleif_invalid_legal_name_post(self):
        """
            Test to see if the GLEIF API post missing data fill is not valid
            for an invalid lei
        """
        response = self.client.post(self.bond_url,
                                    data=json.dumps(invalidLeiPostBondData),
                                    content_type='raw')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_gleif_invalid_legal_name_post(self):
        """
            Test to see if the GLEIF API post missing data fill is not valid
            for a missing lei
        """
        response = self.client.post(self.bond_url,
                                    data=json.dumps(invalidMissingDataPostBondData),
                                    content_type='raw')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
