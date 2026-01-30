import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_platform.settings')
django.setup()

from core.models import User
from projects.models import Project, Task
from reports.models import Notification
from django.utils import timezone
from datetime import timedelta

def populate():
    # Create Users
    admin, _ = User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com', 'role':'ADMIN', 'is_staff':True, 'is_superuser':True})
    admin.set_password('adminpass')
    admin.save()

    manager, _ = User.objects.get_or_create(username='manager', defaults={'email':'manager@example.com', 'role':'MANAGER'})
    manager.set_password('managerpass')
    manager.save()

    employee, _ = User.objects.get_or_create(username='employee', defaults={'email':'employee@example.com', 'role':'EMPLOYEE'})
    employee.set_password('employeepass')
    employee.save()

    print("Users created/verified.")

    # Create Projects
    project1, _ = Project.objects.get_or_create(
        name='Website Redesign',
        defaults={
            'description': 'Overhaul of the company website.',
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date() + timedelta(days=30),
            'status': 'IN_PROGRESS',
            'manager': manager
        }
    )
    print(f"Project '{project1.name}' created.")

    # Create Tasks
    task1, _ = Task.objects.get_or_create(
        title='Design Mockups',
        project=project1,
        defaults={
            'description': 'Create Figma mockups for homepage.',
            'priority': 'HIGH',
            'status': 'IN_PROGRESS',
            'due_date': timezone.now().date() + timedelta(days=5),
            'assigned_to': employee
        }
    )
    print(f"Task '{task1.title}' created.")

    # Create Notification
    notif, _ = Notification.objects.get_or_create(
        user=manager,
        defaults={
            'message': f"Task '{task1.title}' assigned to {employee.username}."
        }
    )
    print(f"Notification created.")

if __name__ == '__main__':
    populate()
