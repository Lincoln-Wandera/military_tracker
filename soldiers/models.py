from django.db import models
from units.models import Unit 
from accounts.models import CustomUser

class Soldier(models.Model):
    SERVICE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('injured', 'Injured'),
        ('mia', 'Missing In Action'),
        ('discharged', 'Discharged'),        
    ]
    service_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    rank = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    current_status = models.CharField(max_length=20, choices=SERVICE_STATUS_CHOICES, default='active')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.current_status

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        from .models import StatusHistory
        if not is_new and self.current_status != self._original_status:
            StatusHistory.objects.create(
                soldier=self,
                status_type=self.current_status,
                updated_by=self.updated_by if hasattr(self, 'updated_by') else None,
                remarks=f"Status changed from {self._original_status} to {self.current_status}",
                status_description="Auto-logged status update"
            )
    def __str__(self):
        return f"{self.rank} {self.first_name} {self.last_name} - {self.service_id}"


class EmergencyContact(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE, related_name='emergency_contacts')
    contact_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contact_name} ({self.relationship})"

class StatusHistory(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    status_type = models.CharField(max_length=20, choices=Soldier.SERVICE_STATUS_CHOICES)
    status_description = models.TextField(blank=True)
    status_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.soldier} - {self.status_type} on {self.status_date}"



class FamilyMember(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'family'})
    relationship = models.CharField(max_length=50)
    is_emergency_contact = models.BooleanField(default=False)
    can_receive_notifications = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} ({self.relationship} of {self.soldier})"
