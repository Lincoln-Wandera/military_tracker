from django.contrib import admin
from .models import Soldier, EmergencyContact, StatusHistory, FamilyMember

@admin.register(Soldier)
class SoldierAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'first_name', 'last_name', 'rank', 'current_status', 'unit')
    search_fields = ('first_name', 'last_name', 'service_id')
    list_filter = ('current_status', 'unit')
    
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'soldier', 'relationship', 'phone_number', 'is_primary')
    
@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('soldier', 'status_type', 'status_date', 'updated_by')
    readonly_fields = ('status_date',)  

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'soldier', 'relationship', 'can_receive_notifications', 'is_active')
    list_filter = ('is_active', 'can_receive_notifications')
    search_fields = ('user__username', 'soldier__first_name', 'soldier__last_name')
