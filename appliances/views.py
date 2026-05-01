from rest_framework import generics
from .models import Appliance
from .serializers import ApplianceSerializer


class ApplianceListCreateView(generics.ListAPIView):
    queryset = Appliance.objects.filter(is_active=True)
    serializer_class = ApplianceSerializer
