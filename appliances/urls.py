# appliances/urls.py

from django.urls import path
from .views import ApplianceListCreateView

urlpatterns = [
    path("", ApplianceListCreateView.as_view(), name="appliance-list"),
]