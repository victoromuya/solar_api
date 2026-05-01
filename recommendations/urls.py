# recommendations/urls.py

from django.urls import path
from .views import RecommendationDetailView

urlpatterns = [
    path("<int:pk>/", RecommendationDetailView.as_view(), name="recommendation-detail"),
]