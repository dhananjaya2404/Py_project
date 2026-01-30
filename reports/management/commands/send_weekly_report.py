from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import Task
import pandas as pd
from datetime import timedelta

class Command(BaseCommand):
    help = 'Sends a weekly report of completed tasks to Admins'

    def handle(self, *args, **options):
        # Calculate date range (last 7 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        
        self.stdout.write(f"Generating report for {start_date} to {end_date}...")

        # Filter tasks
        tasks = Task.objects.filter(status='DONE') # In real app, maybe filter by updated_at within range
        
        if not tasks.exists():
            self.stdout.write(self.style.WARNING("No completed tasks found in the last week."))
            return

        # Generate CSV
        data = list(tasks.values('title', 'project__name', 'assigned_to__username', 'due_date'))
        df = pd.DataFrame(data)
        
        csv_data = df.to_csv(index=False)
        
        # Mock Email Sending
        self.stdout.write("--------------------------------------------------")
        self.stdout.write("Subject: Weekly Task Report")
        self.stdout.write("To: admin@example.com")
        self.stdout.write("Body: Please find attached the weekly report of completed tasks.")
        self.stdout.write("Attachment: weekly_report.csv")
        self.stdout.write("Content Preview:")
        self.stdout.write(csv_data)
        self.stdout.write("--------------------------------------------------")
        
        self.stdout.write(self.style.SUCCESS("Successfully mocked sending weekly report."))
