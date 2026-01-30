from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, LoginForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif user.role == 'MANAGER':
        return redirect('manager_dashboard')
    elif user.role == 'EMPLOYEE':
        return redirect('employee_dashboard')
    return redirect('login')

@login_required
def manager_dashboard(request):
    return render(request, 'core/manager_dashboard.html')

@login_required
def admin_dashboard(request):
    # Only allow ADMINs
    if request.user.role != 'ADMIN':
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return render(request, 'core/admin_dashboard.html')

@login_required
def employee_dashboard(request):
    return render(request, 'core/employee_dashboard.html')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'core/profile_form.html'
    success_url = reverse_lazy('profile_edit')

    def get_object(self):
        return self.request.user

