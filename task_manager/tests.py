from django.test import Client, TestCase
from task_manager.models import User


class SimpleTestCase(TestCase):
    fixtures = ['users.json']

    def test_header(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Менеджер задач")

    def test_user_create(self):
        client = Client()
        client.post('/users/create/',
                    {'first_name': 'john2',
                     'last_name': 'john2',
                     'username': 'john2',
                     'password': '12345678'})
        response = client.get('/users/')
        self.assertContains(response, "john2")

    def test_user_login(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        response = client.get('/')
        self.assertContains(response, "12345")

    def test_user_logout(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        response = client.get('/')
        self.assertContains(response, "12345")
        client.get('/logout/')
        response = client.get('/')
        self.assertNotContains(response, "12345")

    def test_user_update(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        user = User.objects.get(username='12345')
        client.post(f'/users/{user.id}/update/',
                    {'first_name': 'john3',
                     'last_name': 'john3',
                     'username': 'john3',
                     'password': '12345678',
                     'password_confirmation': '12345678', })
        response = client.get('/users/')
        self.assertContains(response, "john3")

    def test_user_delete(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        user = User.objects.get(username='12345')
        client.post(f'/users/{user.id}/delete/',
                    {'id': user.id})
        response = client.get('/users/')
        self.assertNotContains(response, "12345")
