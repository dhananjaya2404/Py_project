from django import forms
from projects.models import Task
from core.models import User

class ReportFilterForm(forms.Form):
    status = forms.ChoiceField(choices=[('', 'All')] + list(Task.STATUS_CHOICES), required=False)
    priority = forms.ChoiceField(choices=[('', 'All')] + list(Task.PRIORITY_CHOICES), required=False)
    assigned_to = forms.ModelChoiceField(queryset=User.objects.filter(role='EMPLOYEE'), required=False, empty_label="All Employees")
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
