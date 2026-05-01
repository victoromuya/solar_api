# recommendations/admin_serializers.py

from rest_framework import serializers
from .models import Recommendation
from .costing import estimate_recommendation_costs


class RecommendationAdminSerializer(serializers.ModelSerializer):
    inverter_estimated_cost_naira = serializers.SerializerMethodField()
    battery_estimated_cost_naira = serializers.SerializerMethodField()
    panel_estimated_cost_naira = serializers.SerializerMethodField()
    total_estimated_cost_naira = serializers.SerializerMethodField()
    cost_note = serializers.SerializerMethodField()
    cost_source_type = serializers.SerializerMethodField()
    cost_source = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = "__all__"

    def _costs(self, obj):
        return estimate_recommendation_costs(obj)

    def get_inverter_estimated_cost_naira(self, obj):
        return self._costs(obj)["inverter_estimated_cost_naira"]

    def get_battery_estimated_cost_naira(self, obj):
        return self._costs(obj)["battery_estimated_cost_naira"]

    def get_panel_estimated_cost_naira(self, obj):
        return self._costs(obj)["panel_estimated_cost_naira"]

    def get_total_estimated_cost_naira(self, obj):
        return self._costs(obj)["total_estimated_cost_naira"]

    def get_cost_note(self, obj):
        return self._costs(obj)["cost_note"]

    def get_cost_source_type(self, obj):
        return self._costs(obj)["cost_source_type"]

    def get_cost_source(self, obj):
        return self._costs(obj)["cost_source"]
