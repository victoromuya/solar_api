# recommendations/admin_views.py

from rest_framework.viewsets import ModelViewSet
from .models import Recommendation
from .admin_serializers import RecommendationAdminSerializer
from core.permissions import IsAdminUserCustom


class RecommendationAdminViewSet(ModelViewSet):
    queryset = Recommendation.objects.all().order_by("-created_at")
    serializer_class = RecommendationAdminSerializer
    permission_classes = [IsAdminUserCustom]