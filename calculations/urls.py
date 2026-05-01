# calculations/urls.py

from django.urls import path
from .views import CalculationCreateView, CalculationDetailView

urlpatterns = [
    path("", CalculationCreateView.as_view(), name="create-calculation"),
    path("<int:pk>/", CalculationDetailView.as_view(), name="calculation-detail"),
]