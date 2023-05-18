from django.test import Client, TestCase
from task_manager.statuses.models import Status
from django.urls import reverse


class SimpleTestCase(TestCase):
    fixtures = ['fixtures/dump.json']

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