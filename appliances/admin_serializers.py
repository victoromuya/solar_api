# appliances/admin_serializers.py

from rest_framework import serializers
from .models import Appliance


class ApplianceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = "__all__"