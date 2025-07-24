from django.contrib import admin
from .models import Mission, SoldierMission

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('mission_name', 'mission_code', 'location', 'mission_status')
    search_fields = ('mission_name', 'mission_code')

@admin.register(SoldierMission)
class SoldierMissionAdmin(admin.ModelAdmin):
    list_display = ('soldier', 'mission', 'assigned_date', 'assignment_status')
    list_filter = ('assignment_status',)
