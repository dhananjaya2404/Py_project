from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Project, Task
from .forms import ProjectForm, TaskForm

class ManagerCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'MANAGER']

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm
from .comment_forms import CommentForm
from .utils import get_ai_prioritization, analyze_sentiment

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.all()
        # Add AI Insights
        context['ai_prioritization'] = get_ai_prioritization(tasks)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'add_comment' in request.POST:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.task = task
                comment.author = request.user
                comment.sentiment = analyze_sentiment(comment.content)
                comment.save()
                return redirect('project_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)


class ProjectCreateView(LoginRequiredMixin, ManagerCheckMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

class ProjectUpdateView(LoginRequiredMixin, ManagerCheckMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

class ProjectDeleteView(LoginRequiredMixin, ManagerCheckMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

class TaskCreateView(LoginRequiredMixin, ManagerCheckMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['project_id']})

class TaskUpdateView(LoginRequiredMixin, ManagerCheckMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})

class TaskDeleteView(LoginRequiredMixin, ManagerCheckMixin, DeleteView):
    model = Task
    template_name = 'projects/task_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})

class EmployeeTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'projects/employee_task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by('due_date')

class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['status']
    template_name = 'projects/task_status_update.html'
    success_url = reverse_lazy('employee_task_list')

    def get_queryset(self):
        # Allow employees to update status of their own tasks
        return Task.objects.filter(assigned_to=self.request.user)
