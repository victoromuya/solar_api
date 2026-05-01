# project/admin_api_urls.py

from rest_framework.routers import DefaultRouter

from appliances.admin_views import ApplianceAdminViewSet
from calculations.admin_views import CalculationAdminViewSet
from recommendations.admin_views import RecommendationAdminViewSet


router = DefaultRouter()
router.register(r"appliances", ApplianceAdminViewSet)
router.register(r"calculations", CalculationAdminViewSet)
router.register(r"recommendations", RecommendationAdminViewSet)

urlpatterns = router.urls