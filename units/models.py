from django.db import models

class Unit(models.Model):
    unit_name = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=20, unique=True)
    base_location = models.CharField(max_length=100)
    commander_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.unit_name} ({self.unit_code})"
