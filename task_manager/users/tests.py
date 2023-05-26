from django.test import Client, TestCase
from task_manager.users.models import User
from task_manager.tests import get_test_data
from django.utils.translation import gettext as _


class UserTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()
        self.login_user = \
            User.objects.get(username=self.test_data['login_username'])
        self.used_user = \
            User.objects.get(username=self.test_data['login_used_username'])
        self.client = Client()

    def test_user_create(self):
        self.client.post('/users/create/',
                         self.test_data['create_user_data'])
        response = self.client.get('/users/')
        self.assertContains(response,
                            self.test_data["create_user_result"])
        self.assertContains(response,
                            _('User created'))

    def test_user_update(self):
        self.client.force_login(self.login_user)
        user = User.objects.get(username=self.test_data['update_user'])
        self.client.post(f'/users/{user.id}/update/',
                         self.test_data['update_user_data'])
        response = self.client.get('/users/')
        self.assertContains(response, self.test_data['update_user_result'])
        self.assertContains(response, _('User changed'))

    def test_user_delete(self):
        self.client.post('/users/create/',
                         self.test_data['create_user_data'])
        deleted_user = User.objects.get(username=self.test_data['delete_user'])
        self.client.force_login(deleted_user)
        self.client.post(f'/users/{deleted_user.id}/delete/',
                         self.test_data['delete_user_data'])
        response = self.client.get('/users/')
        self.assertNotContains(response, self.test_data['delete_user'])
        self.assertContains(response, _('User deleted'))

    def test_delete_used_user(self):
        self.client.force_login(self.used_user)
        user = User.objects.get(username=self.test_data['used_user'])
        self.client.post(f'/users/{user.id}/delete/',
                         self.test_data['delete_used_user_data'])
        response = self.client.get('/users/')
        self.assertContains(response, self.test_data['used_user'])
        self.assertContains(response, _("Can't delete used user"))

    def test_create_already_exist_user(self):
        response = self.client.post('/users/create/',
                                    self.test_data['existed_user_data'])
        self.assertContains(response, _("User already exist"))
