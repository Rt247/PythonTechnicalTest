from rest_framework import serializers

from .models import Bond

class BondSerializer(serializers.ModelSerializer):
    """
        Bond Serializer transforms everything bar the user
    """
    class Meta:
        model = Bond
        fields = [
            'isin',
            'size',
            'currency',
            'maturity',
            'lei',
            'legal_name'
        ]





