from django.contrib import admin

from .models import Unit

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_name', 'unit_code', 'base_location', 'commander_name', 'is_active')
    search_fields = ('unit_name', 'unit_code', 'commander_name')
    list_filter = ('is_active',)   