from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import CustomUser
from .models import StatusHistory, FamilyMember
from notifications.models import Notification
from django.utils.timezone import now


@receiver(post_save, sender=StatusHistory)
def notify_family_on_status_change(sender, instance, created, **kwargs):
    if not created:
        return

    soldier = instance.soldier
    family_members = FamilyMember.objects.filter(soldier=soldier, can_receive_notifications=True, is_active=True)

    for fm in family_members:
        Notification.objects.create(
            soldier=soldier,
            family=fm.user,
            notification_type='status_change',
            subject=f"Status Update: {soldier.first_name} {soldier.last_name}",
            message=f"The status of {soldier.first_name} {soldier.last_name} has changed to '{instance.status_type}'.\n\nRemarks: {instance.remarks or 'None'}",
            delivery_method='system',
            is_sent=True,
            sent_at=now()
        )
        
@receiver(post_save, sender=FamilyMember)
def notify_admin_on_family_link(sender, instance, created, **kwargs):
    if created:
        # Send email to all active admins
        admin_emails = CustomUser.objects.filter(role='admin', is_active=True).values_list('email', flat=True)
        send_mail(
            subject="🔔 New Family Link Created",
            message=f"{instance.user.get_full_name()} ({instance.user.email}) linked to soldier {instance.soldier}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email for email in admin_emails if email],
            fail_silently=True,
        )
