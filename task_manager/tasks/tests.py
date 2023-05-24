from django.test import Client, TestCase
from task_manager.tasks.models import Task
from task_manager.tests import get_test_data
from django.urls import reverse
from django.utils.translation import gettext as _


class TaskTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()

    def test_task_create(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        client.post(reverse('task_create'),
                    self.test_data['create_task_data'])
        response = client.get('/tasks/')
        self.assertContains(response,
                            self.test_data['create_task_result'])
        self.assertContains(response,
                            _('Task created'))

    def test_task_update(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        task = Task.objects.get(name=self.test_data['update_task'])
        client.post(f'/tasks/{task.id}/update/',
                    self.test_data['update_task_data'])
        response = client.get('/tasks/')
        self.assertContains(response, self.test_data['update_task_result'])
        self.assertContains(response, _('Task changed'))

    def test_task_delete(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        task = Task.objects.get(name=self.test_data['delete_task'])
        client.post(f'/tasks/{task.id}/delete/',
                    self.test_data['delete_task_data'])
        response = client.get('/tasks/')
        self.assertNotContains(response, self.test_data['delete_task'])
        self.assertContains(response, _('Task deleted'))
