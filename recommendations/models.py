from django.db import models
from calculations.models import Calculation

class Recommendation(models.Model):
    calculation = models.OneToOneField(
        Calculation,
        related_name="recommendation",
        on_delete=models.CASCADE
    )

    inverter_kva = models.FloatField()
    inverter_note = models.CharField(max_length=255)

    battery_capacity_ah = models.FloatField()
    battery_recommendation = models.CharField(max_length=255)

    solar_total_watts = models.FloatField()
    panel_size_watts = models.IntegerField(default=200)
    panel_quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for Calculation #{self.calculation.id}"
    
    
class RecommendationTier(models.Model):
    TIER_CHOICES = [
        ("budget", "Budget"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    recommendation = models.ForeignKey(
        Recommendation,
        related_name="tiers",
        on_delete=models.CASCADE
    )

    tier = models.CharField(max_length=20, choices=TIER_CHOICES)

    inverter = models.CharField(max_length=50)
    battery = models.CharField(max_length=50)
    solar_panels = models.CharField(max_length=50)

    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tier} Tier - Calc #{self.recommendation.calculation.id}"