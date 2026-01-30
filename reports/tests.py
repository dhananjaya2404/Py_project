from django.test import TestCase
from reports.models import Notification, ActivityLog
from core.models import User

class ReportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='notif_user', password='p')

    def test_notification(self):
        n = Notification.objects.create(user=self.user, message='Test')
        self.assertEqual(n.message, 'Test')

    def test_activity_log(self):
        log = ActivityLog.objects.create(actor=self.user, action='LOGIN', target_model='User', target_repr='notif_user')
        self.assertEqual(log.action, 'LOGIN')
