# calculations/admin_views.py

from rest_framework.viewsets import ModelViewSet
from .models import Calculation
from .admin_serializers import CalculationAdminSerializer
from core.permissions import IsAdminUserCustom


class CalculationAdminViewSet(ModelViewSet):
    queryset = Calculation.objects.all().order_by("-created_at")
    serializer_class = CalculationAdminSerializer
    permission_classes = [IsAdminUserCustom]