from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'issue_details', 'issue_type', 'location', 'status', 'created_at')
    list_filter = ('issue_type', 'status', 'created_at')
    search_fields = ('reference_number', 'issue_details', 'location')
    readonly_fields = ('reference_number', 'created_at', 'updated_at')