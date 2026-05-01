from django.db.models.signals import post_save
from django.dispatch import receiver

from calculations.models import Calculation
from recommendations.models import Recommendation
from calculations.service import SolarCalculationService


@receiver(post_save, sender=Calculation)
def create_recommendation(sender, instance, created, **kwargs):
    if not created:
        return

    if not instance.appliances.exists():
        return  # wait until appliances are added

    data = SolarCalculationService.calculate(instance)

    Recommendation.objects.create(
        calculation=instance,
        inverter_kva=data["inverter_kva"],
        inverter_note="Recommended minimum inverter size",
        battery_capacity_ah=data["battery_ah"],
        battery_recommendation=f"{round(data['battery_ah']/200)} x 200Ah batteries",
        solar_total_watts=data["panel_total_watts"],
        panel_size_watts=200,
        panel_quantity=data["panel_qty"],
    )