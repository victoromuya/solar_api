from rest_framework import generics
from .models import Calculation
from .serializers import CalculationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from recommendations.serializers import RecommendationSerializer
from django.shortcuts import get_object_or_404


class CalculationCreateView(generics.CreateAPIView):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer


class CalculationDetailView(APIView):
    def get(self, request, pk):
        calculation = get_object_or_404(Calculation, pk=pk)

        calc_data = CalculationSerializer(calculation).data

        recommendation = getattr(calculation, "recommendation", None)
        rec_data = RecommendationSerializer(recommendation).data if recommendation else None

        return Response({
            "calculation": calc_data,
            "recommendation": rec_data
        })
