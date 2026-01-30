from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from projects.models import Task
from .forms import ReportFilterForm
from .models import Report, Notification, ActivityLog
import pandas as pd
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'reports/notification_list.html'
    context_object_name = 'notifications'
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class MarkNotificationReadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return redirect('notification_list')

class ReportDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'MANAGER']

    def get(self, request):
        form = ReportFilterForm(request.GET)
        tasks = Task.objects.all()

        if form.is_valid():
            if form.cleaned_data['status']:
                tasks = tasks.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['priority']:
                tasks = tasks.filter(priority=form.cleaned_data['priority'])
            if form.cleaned_data['assigned_to']:
                tasks = tasks.filter(assigned_to=form.cleaned_data['assigned_to'])
            if form.cleaned_data['date_from']:
                tasks = tasks.filter(due_date__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                tasks = tasks.filter(due_date__lte=form.cleaned_data['date_to'])
        
        return render(request, 'reports/report_dashboard.html', {'form': form, 'tasks': tasks})

class ExportReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'MANAGER']

    def get(self, request, fmt):
        # Apply filters (same logic - duplicating for now, ideally refactor to service/mixin)
        form = ReportFilterForm(request.GET)
        tasks = Task.objects.all()
        if form.is_valid():
            if form.cleaned_data.get('status'):
                tasks = tasks.filter(status=form.cleaned_data['status'])
            if form.cleaned_data.get('priority'):
                tasks = tasks.filter(priority=form.cleaned_data['priority'])
            if form.cleaned_data.get('assigned_to'):
                tasks = tasks.filter(assigned_to=form.cleaned_data['assigned_to'])
            if form.cleaned_data.get('date_from'):
                tasks = tasks.filter(due_date__gte=form.cleaned_data['date_from'])
            if form.cleaned_data.get('date_to'):
                tasks = tasks.filter(due_date__lte=form.cleaned_data['date_to'])

        # Pandas DataFrame
        data = list(tasks.values('title', 'project__name', 'assigned_to__username', 'status', 'priority', 'due_date'))
        df = pd.DataFrame(data)

        if fmt == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="tasks_report.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response
        
        elif fmt == 'excel':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="tasks_report.xlsx"'
            df.to_excel(response, index=False)
            return response

        elif fmt == 'pdf':
            template = get_template('reports/pdf_template.html')
            context = {'tasks': tasks}
            html = template.render(context)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="tasks_report.pdf"'
                return response
            return HttpResponse('Error generating PDF', status=500)

        return HttpResponse('Invalid format', status=400)

class ActivityLogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ActivityLog
    template_name = 'reports/activity_log_list.html'
    context_object_name = 'logs'
    paginate_by = 20

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def get_queryset(self):
        return ActivityLog.objects.all().order_by('-timestamp')

