from django.db import models


class Calculation(models.Model):
    SYSTEM_VOLTAGE_CHOICES = [
        (12, "12V"),
        (24, "24V"),
        (48, "48V"),
    ]

    user_identifier = models.CharField(
        max_length=100, blank=True, null=True
    )

    backup_hours = models.FloatField(default=5)
    system_voltage = models.IntegerField(choices=SYSTEM_VOLTAGE_CHOICES, default=12)
    sunlight_hours = models.FloatField(default=5)

    # Computed values
    total_load_watts = models.FloatField(blank=True, null=True)
    adjusted_load_watts = models.FloatField(blank=True, null=True)
    daily_energy_wh = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calculation #{self.id} - {self.total_load_watts}W"
    

class CalculationAppliance(models.Model):
    calculation = models.ForeignKey(
        Calculation,
        related_name="appliances",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    watts = models.FloatField()
    hours_per_day = models.FloatField()

    def total_power(self):
        return self.quantity * self.watts

    def daily_energy(self):
        return self.total_power() * self.hours_per_day

    def __str__(self):
        return f"{self.name} x{self.quantity}"