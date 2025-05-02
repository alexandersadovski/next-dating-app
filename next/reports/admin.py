from django.contrib import admin
from next.reports.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_by', 'reported_user', 'reason', 'created_at', 'status')
    list_filter = ('reason', 'status', 'created_at')
    search_fields = ('reported_by__email', 'reported_user__email')
    ordering = ('-created_at',)
