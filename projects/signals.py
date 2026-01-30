from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from reports.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Task)
def create_notification_on_assignment(sender, instance, created, **kwargs):
    if instance.assigned_to:
        # Check if it was created or if assignment changed (simplification: just notify on creation for now, 
        # tracking field changes requires pre_save or other logic)
        if created:
            Notification.objects.create(
                user=instance.assigned_to,
                message=f"You have been assigned a new task: '{instance.title}' in project '{instance.project.name}'."
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.assigned_to.id}",
                {
                    "type": "send_notification",
                    "message": f"You have been assigned a new task: '{instance.title}'"
                }
            )

@receiver(post_save, sender=Task)
def create_notification_on_status_change(sender, instance, created, **kwargs):
    if not created:
        # Simplification: In a real app we'd check if status specifically field changed.
        # Here we assume any update might be status update.
        # Notify the project manager (if it's not the manager updating it themselves - skipping that check for simplicity)
        manager = instance.project.manager
        Notification.objects.create(
            user=manager,
            message=f"Task '{instance.title}' status updated to '{instance.get_status_display()}' by {instance.assigned_to}"
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{manager.id}",
            {
                "type": "send_notification",
                "message": f"Task '{instance.title}' updated to '{instance.get_status_display()}'"
            }
        )
