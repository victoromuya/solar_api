from rest_framework import serializers
from math import ceil

from calculations.service import SolarCalculationService
from recommendations.models import Recommendation
from .models import Calculation, CalculationAppliance


class CalculationApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationAppliance
        fields = ["id", "name", "quantity", "watts", "hours_per_day"]
        read_only_fields = ["id"]


class CalculationSerializer(serializers.ModelSerializer):
    appliances = CalculationApplianceSerializer(many=True)

    class Meta:
        model = Calculation
        fields = [
            "id",
            "backup_hours",
            "system_voltage",
            "sunlight_hours",
            "total_load_watts",
            "adjusted_load_watts",
            "daily_energy_wh",
            "appliances",
        ]
        read_only_fields = [
            "id",
            "total_load_watts",
            "adjusted_load_watts",
            "daily_energy_wh",
        ]

    def validate(self, attrs):
        appliances = attrs.get("appliances", [])

        if not appliances:
            raise serializers.ValidationError(
                {"appliances": "Add at least one appliance."}
            )

        if attrs.get("backup_hours", 0) <= 0:
            raise serializers.ValidationError(
                {"backup_hours": "Backup hours must be greater than zero."}
            )

        if attrs.get("sunlight_hours", 0) <= 0:
            raise serializers.ValidationError(
                {"sunlight_hours": "Sunlight hours must be greater than zero."}
            )

        return attrs

    def create(self, validated_data):
        appliances_data = validated_data.pop("appliances")
        calculation = Calculation.objects.create(**validated_data)

        for appliance_data in appliances_data:
            CalculationAppliance.objects.create(
                calculation=calculation,
                **appliance_data,
            )

        data = SolarCalculationService.calculate(calculation)
        calculation.total_load_watts = data["total_watts"]
        calculation.adjusted_load_watts = data["adjusted_load"]
        calculation.daily_energy_wh = data["daily_energy"]
        calculation.save(
            update_fields=[
                "total_load_watts",
                "adjusted_load_watts",
                "daily_energy_wh",
            ]
        )

        Recommendation.objects.create(
            calculation=calculation,
            inverter_kva=data["inverter_kva"],
            inverter_note="Recommended minimum inverter size",
            battery_capacity_ah=data["battery_ah"],
            battery_recommendation=f"{max(1, ceil(data['battery_ah'] / 200))} x 200Ah batteries",
            solar_total_watts=data["panel_total_watts"],
            panel_size_watts=SolarCalculationService.PANEL_SIZE,
            panel_quantity=data["panel_qty"],
        )

        return calculation
