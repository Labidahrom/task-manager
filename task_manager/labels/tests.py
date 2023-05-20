from django.test import Client, TestCase
from task_manager.labels.models import Label
from task_manager.tests import get_test_data


TEST_DATA = get_test_data()


class LabelTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def test_label_create(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        client.post('/labels/create/',
                    TEST_DATA['create_label_data'])
        response = client.get('/labels/')
        self.assertContains(response,
                            TEST_DATA["create_label_result"])
        self.assertContains(response,
                            TEST_DATA["create_label_message"])

    def test_label_update(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        label = Label.objects.get(name=TEST_DATA['update_label'])
        client.post(f'/labels/{label.id}/update/',
                    TEST_DATA['update_label_data'])
        response = client.get('/labels/')
        self.assertContains(response, TEST_DATA['update_label_result'])
        self.assertContains(response, TEST_DATA['update_label_message'])

    def test_label_delete(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        label = Label.objects.get(name=TEST_DATA['delete_label'])
        client.post(f'/labels/{label.id}/delete/',
                    TEST_DATA['delete_label_data'])
        response = client.get('/labels/')
        self.assertNotContains(response, TEST_DATA['delete_label'])
        self.assertContains(response, TEST_DATA['delete_label_message'])
