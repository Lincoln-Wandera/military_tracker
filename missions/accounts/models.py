from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('family', 'Family'),
    ]
    role = models.CharField(max_length=10, default='family')
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class FamilyMember(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='family_member')
    relationship = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Family Member ({self.relationship})"

