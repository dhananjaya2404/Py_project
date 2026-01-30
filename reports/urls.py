from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/read/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('dashboard/', views.ReportDashboardView.as_view(), name='report_dashboard'),
    path('export/<str:fmt>/', views.ExportReportView.as_view(), name='export_report'),
    path('logs/', views.ActivityLogListView.as_view(), name='activity_logs'),
]
