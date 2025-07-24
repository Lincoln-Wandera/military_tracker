from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'soldier', 'family', 'delivery_method', 'is_sent', 'sent_at')
    list_filter = ('is_sent', 'delivery_method', 'notification_type')
    search_fields = ('subject', 'message')
