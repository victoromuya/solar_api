# calculations/admin_serializers.py

from rest_framework import serializers
from .models import Calculation, CalculationAppliance


class CalculationApplianceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationAppliance
        fields = "__all__"


class CalculationAdminSerializer(serializers.ModelSerializer):
    appliances = CalculationApplianceAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Calculation
        fields = "__all__"