import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.http import Http404
from django.http.response import JsonResponse

from .models import Bond
from .serializers import BondSerializer
from .thirdpartyapis import get_legal_name

class BondsListView(APIView):
    """
        View for POST a bond and GET a list of bonds
        Bonds are linked to the user in the input authorization tokens header
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            Get the list of user bonds as a JSON
            Filter implemented for all valid parameters
            Return all bond data bar the user defined in the serializer
        """

        try:
            valid_filters = ['isin',
                             'size',
                             'currency',
                             'maturity',
                             'lei',
                             'legal_name']

            filters = {key: value for key, value in self.request.query_params.items() if key in valid_filters}

            bondsList = Bond.objects.all()
            bondsList = Bond.objects.filter(user=request.user).values()
            bondsList = bondsList.filter(**filters)

            bonds_serializer = BondSerializer(bondsList, many=True)

            return JsonResponse(bonds_serializer.data, safe=False)

        except Bond.DoesNotExist:
            raise Http404("Bonds do not exist in database")


    def post(self, request):
        """
            Post bond data if valid in serializer
        """

        bond_data = JSONParser().parse(request)
        bonds_serializer = BondSerializer(data=bond_data)

        if bonds_serializer.is_valid():
            bonds_serializer.save()
            return JsonResponse(bonds_serializer.data, status=status.HTTP_201_CREATED)

        # Attempt to fill in legal name data if possible
        err_legal_name = bonds_serializer.errors.get("legal_name", None)
        err_lei = bonds_serializer.errors.get("lei", None)

        if "This field is required." in err_legal_name and not err_lei:
            legal_name = get_legal_name(bonds_serializer.data['lei'])

            # Process only if legal_name is correctly fetched from third party api
            if legal_name:
                updated_data = bonds_serializer.data
                updated_data['legal_name'] = legal_name

                bonds_serializer = BondSerializer(data=updated_data)

                if bonds_serializer.is_valid():
                    bonds_serializer.save(user=self.request.user)
                    return JsonResponse(bonds_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(bonds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



