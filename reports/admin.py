from django.contrib import admin
from .models import Report, Notification

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'generated_by', 'created_at')
    list_filter = ('generated_by', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
