from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from projects.models import Project, Task
import pandas as pd
import json

class AnalyticsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def test_func(self):
        # Temporarily allowing all roles for UI review
        return self.request.user.role in ['ADMIN', 'MANAGER', 'EMPLOYEE']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch data
        projects = Project.objects.all().values('id', 'name', 'manager__username')
        tasks = Task.objects.all().values('id', 'status', 'priority', 'project__name', 'due_date')

        # Convert to DataFrames
        df_projects = pd.DataFrame(list(projects))
        df_tasks = pd.DataFrame(list(tasks))

        if df_tasks.empty:
            context['no_data'] = True
            return context

        # 1. KPI: Totals
        context['total_projects'] = len(df_projects)
        context['total_tasks'] = len(df_tasks)
        
        # 2. KPI: Tasks by Status
        status_counts = df_tasks['status'].value_counts()
        context['status_labels'] = json.dumps(list(status_counts.index))
        context['status_data'] = json.dumps([int(x) for x in status_counts.values])

        # 3. KPI: Tasks by Priority
        priority_counts = df_tasks['priority'].value_counts()
        context['priority_labels'] = json.dumps(list(priority_counts.index))
        context['priority_data'] = json.dumps([int(x) for x in priority_counts.values])

        # 4. Project Completion Analysis
        # Count total tasks per project
        project_task_counts = df_tasks.groupby('project__name')['id'].count().rename('total_tasks')
        
        # Count completed tasks per project
        completed_tasks = df_tasks[df_tasks['status'] == 'DONE'].groupby('project__name')['id'].count().rename('completed_tasks')
        
        # Merge and calculate percentage
        df_progress = pd.concat([project_task_counts, completed_tasks], axis=1).fillna(0)
        df_progress['completion_rate'] = (df_progress['completed_tasks'] / df_progress['total_tasks'] * 100).round(1)
        
        # Convert to list of dicts for template
        context['project_progress'] = df_progress.reset_index().to_dict('records')

        # 5. AI Suggestions (Top 5 Urgent)
        all_tasks = Task.objects.all()
        from projects.utils import get_ai_prioritization
        context['ai_suggestions'] = get_ai_prioritization(all_tasks)[:5]

        # 6. Sentiment Analysis Summary
        from projects.models import Comment
        recent_comments = Comment.objects.order_by('-created_at')[:10]
        context['recent_comments'] = recent_comments
        
        return context

