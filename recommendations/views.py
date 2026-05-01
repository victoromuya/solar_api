from rest_framework import generics
from .models import Recommendation
from .serializers import RecommendationSerializer


class RecommendationDetailView(generics.RetrieveAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer