from django.test import Client, TestCase
from task_manager.users.models import User
from task_manager.tests import get_test_data


TEST_DATA = get_test_data()


class UserTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def test_user_create(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        client.post('/users/create/',
                    TEST_DATA['create_user_data'])
        response = client.get('/users/')
        self.assertContains(response,
                            TEST_DATA["create_user_result"])

    def test_user_update(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        user = User.objects.get(username=TEST_DATA['update_user'])
        client.post(f'/users/{user.id}/update/',
                    TEST_DATA['update_user_data'])
        response = client.get('/users/')
        self.assertContains(response, TEST_DATA['update_user_result'])

    def test_user_delete(self):
        client = Client()
        client.post('/users/create/',
                    TEST_DATA['create_user_data'])
        client.post('/login/',
                    TEST_DATA['login_deleted_user_data'])
        user = User.objects.get(username=TEST_DATA['delete_user'])
        client.post(f'/users/{user.id}/delete/',
                    TEST_DATA['delete_user_data'])
        response = client.get('/users/')
        self.assertNotContains(response, TEST_DATA['delete_user'])
