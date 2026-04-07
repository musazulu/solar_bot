from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('phone', 'message', 'created_at')
    search_fields = ('phone', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)