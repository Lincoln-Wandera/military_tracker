from django.db import models
from soldiers.models import Soldier
from accounts.models import CustomUser  # for family members

class Notification(models.Model):
    DELIVERY_CHOICES = [
        ('email', 'Email'),
        ('system', 'In-System'),
    ]

    NOTIF_TYPE_CHOICES = [
        ('status_change', 'Status Change'),
        ('mission_update', 'Mission Update'),
        ('general', 'General'),
    ]

    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    family = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'family'})
    notification_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} to {self.family} ({self.delivery_method})"
