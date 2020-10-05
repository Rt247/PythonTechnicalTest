from rest_framework import serializers

from .models import Bond

class BondSerializer(serializers.ModelSerializer):

    #user = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

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





