from django.test import TestCase, Client
from django.urls import reverse
from core.models import User

class CoreTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='password', role='EMPLOYEE')

    def test_login(self):
        response = self.c.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_profile_update(self):
        self.c.login(username='testuser', password='password')
        response = self.c.post(reverse('profile_edit'), {
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'new@example.com',
            'department': 'HR'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'New')
