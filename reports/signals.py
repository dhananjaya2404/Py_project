from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ActivityLog
from projects.models import Project, Task

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ActivityLog.objects.create(actor=user, action='LOGIN', target_model='User', target_repr=user.username)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        ActivityLog.objects.create(actor=user, action='LOGOUT', target_model='User', target_repr=user.username)

@receiver(post_save, sender=Project)
def log_project_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    # Fallback to a system user or handle lack of request context in signals
    # In a real app, you'd use a middleware to capture the current user
    ActivityLog.objects.create(action=action, target_model='Project', target_object_id=instance.id, target_repr=instance.name)

@receiver(post_save, sender=Task)
def log_task_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    ActivityLog.objects.create(action=action, target_model='Task', target_object_id=instance.id, target_repr=instance.title)
