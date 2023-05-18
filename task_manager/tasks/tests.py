from django.test import Client, TestCase
from task_manager.tasks.models import Task
from task_manager.tests import get_test_data
from django.urls import reverse

TEST_DATA = get_test_data()


class TaskTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def test_task_create(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        client.post(reverse('task_create'),
                    TEST_DATA['create_task_data'])
        response = client.get('/tasks/')
        self.assertContains(response,
                            TEST_DATA['create_task_result'])

    def test_task_update(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        task = Task.objects.get(name=TEST_DATA['update_task'])
        client.post(f'/tasks/{task.id}/update/',
                    TEST_DATA['update_task_data'])
        response = client.get('/tasks/')
        self.assertContains(response, TEST_DATA['update_task_result'])

    def test_task_delete(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        task = Task.objects.get(name=TEST_DATA['delete_task'])
        client.post(f'/tasks/{task.id}/delete/',
                    TEST_DATA['delete_task_data'])
        response = client.get('/tasks/')
        self.assertNotContains(response, TEST_DATA['delete_task'])
