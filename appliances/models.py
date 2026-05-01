from django.db import models


class Appliance(models.Model):
    name = models.CharField(max_length=100)
    default_watts = models.FloatField()
    category = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.default_watts}W)"