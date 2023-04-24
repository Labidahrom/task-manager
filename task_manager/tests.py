from django.test import Client, TestCase
from task_manager.models import User, Status, Task, Label
from django.urls import reverse


class SimpleTestCase(TestCase):
    fixtures = ['dump.json']

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
                    {'username': 'afaf',
                     'password': '12345678'})
        user = User.objects.get(username='afaf')
        client.post(f'/users/{user.id}/delete/',
                    {'id': user.id})
        response = client.get('/users/')
        self.assertNotContains(response, "afaf")

    def test_status_create(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        client.post('/statuses/create/',
                    {'name': 'john2'})
        response = client.get('/statuses/')
        self.assertContains(response, "john2")

    def test_status_update(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        status = Status.objects.get(name='Быстро')
        client.post(f'/statuses/{status.id}/update/',
                    {'name': 'Медленно'})
        response = client.get('/statuses/')
        self.assertContains(response, "Медленно")

    def test_status_delete(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        status = Status.objects.get(name='Норма44')
        client.post(f'/statuses/{status.id}/delete/',
                    {'id': status.id})
        response = client.get('/statuses/')
        self.assertNotContains(response, "Норма44")

    def test_task_create(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        assagnee = User.objects.get(username='12345')
        status = Status.objects.get(name='Быстро')
        client.post(reverse('task_create'),
                    {'name': 'john4',
                     'description': 'john3',
                     'assigned_to': assagnee.id,
                     'status': status.id})
        response = client.get('/tasks/')
        self.assertContains(response, "john4")

    def test_task_update(self):
        client = Client()
        client.post('/login/',
                    {'username': 'test',
                     'password': '12345678'})
        task = Task.objects.get(name='test')
        assagnee = User.objects.get(username='12345')
        status = Status.objects.get(name='Норма')
        client.post(reverse('task_update', kwargs={'id': task.id}),
                    {'name': 'john3',
                     'description': 'john3',
                     'assigned_to': assagnee.id,
                     'status': status.id})
        response = client.get('/tasks/')
        self.assertContains(response, "john3")

    def test_task_delete(self):
        client = Client()
        client.post('/login/',
                    {'username': 'ulya',
                     'password': '12345678'})
        task = Task.objects.get(name='test344')
        client.post(f'/tasks/{task.id}/delete/',
                    {'id': task.id})
        response = client.get('/tasks/')
        self.assertNotContains(response, "test344")

    def test_label_create(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        client.post('/labels/create/',
                    {'name': 'john2'})
        response = client.get('/labels/')
        self.assertContains(response, "john2")

    def test_label_update(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        label = Label.objects.get(name='test')
        client.post(f'/labels/{label.id}/update/',
                    {'name': '333'})
        response = client.get('/labels/')
        self.assertContains(response, "333")

    def test_label_delete(self):
        client = Client()
        client.post('/login/',
                    {'username': '12345',
                     'password': '12345678'})
        label = Label.objects.get(name='test3')
        client.post(f'/labels/{label.id}/delete/',
                    {'id': label.id})
        response = client.get('/labels/')
        self.assertNotContains(response, "test3")
