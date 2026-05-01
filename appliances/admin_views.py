# appliances/admin_views.py

from rest_framework.viewsets import ModelViewSet
from .models import Appliance
from .admin_serializers import ApplianceAdminSerializer
from core.permissions import IsAdminUserCustom


class ApplianceAdminViewSet(ModelViewSet):
    queryset = Appliance.objects.all()
    serializer_class = ApplianceAdminSerializer
    permission_classes = [IsAdminUserCustom]