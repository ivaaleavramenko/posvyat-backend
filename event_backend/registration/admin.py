from django.contrib import admin
from .models import Visitor, EventWave, BlackList

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'created_at']
    list_filter = ['created_at']

@admin.register(EventWave)
class EventWaveAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_capacity', 'current_count', 'is_active']

@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'reason']
