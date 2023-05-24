from django.test import Client, TestCase
from task_manager.users.models import User
from task_manager.tests import get_test_data
from django.utils.translation import gettext as _


class UserTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()

    def test_user_create(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        client.post('/users/create/',
                    self.test_data['create_user_data'])
        response = client.get('/users/')
        self.assertContains(response,
                            self.test_data["create_user_result"])
        self.assertContains(response,
                            _('User created'))

    def test_user_update(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        user = User.objects.get(username=self.test_data['update_user'])
        client.post(f'/users/{user.id}/update/',
                    self.test_data['update_user_data'])
        response = client.get('/users/')
        self.assertContains(response, self.test_data['update_user_result'])
        self.assertContains(response, _('User changed'))

    def test_user_delete(self):
        client = Client()
        client.post('/users/create/',
                    self.test_data['create_user_data'])
        client.post('/login/',
                    self.test_data['login_deleted_user_data'])
        user = User.objects.get(username=self.test_data['delete_user'])
        client.post(f'/users/{user.id}/delete/',
                    self.test_data['delete_user_data'])
        response = client.get('/users/')
        self.assertNotContains(response, self.test_data['delete_user'])
        self.assertContains(response, _('User deleted'))

    def test_delete_used_user(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_used_user_data'])
        user = User.objects.get(username=self.test_data['used_user'])
        client.post(f'/users/{user.id}/delete/',
                    self.test_data['delete_used_user_data'])
        response = client.get('/users/')
        self.assertContains(response, self.test_data['used_user'])
        self.assertContains(response, _("Can't delete used user"))
