from django.test import TestCase
from projects.models import Project, Task, Comment
from core.models import User
from projects.utils import analyze_sentiment, get_ai_prioritization
from django.utils import timezone
from datetime import timedelta, date

class ProjectTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username='manager_t', password='p', role='MANAGER')
        self.project = Project.objects.create(
            name='Test P', manager=self.manager,
            start_date=date.today(), end_date=date.today()
        )

    def test_sentiment(self):
        self.assertEqual(analyze_sentiment("This is great"), "POSITIVE")
        self.assertEqual(analyze_sentiment("This is a problem"), "NEGATIVE")

    def test_ai_prioritization(self):
        task = Task.objects.create(
            title='Urgent', project=self.project, priority='HIGH',
            due_date=date.today() + timedelta(days=1), status='TODO'
        )
        results = get_ai_prioritization([task])
        self.assertTrue(results[0]['is_suggested_urgent'])

    def test_comment_creation(self):
        task = Task.objects.create(title='T', project=self.project, due_date=date.today())
        comment = Comment.objects.create(task=task, author=self.manager, content='Test')
        self.assertEqual(comment.task, task)
