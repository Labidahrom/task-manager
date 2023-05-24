from django.test import Client, TestCase
from task_manager.statuses.models import Status
from task_manager.tests import get_test_data
from django.utils.translation import gettext as _


TEST_DATA = get_test_data()


class StatusTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()

    def test_status_create(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        client.post('/statuses/create/',
                    self.test_data['create_status_data'])
        response = client.get('/statuses/')
        self.assertContains(response,
                            self.test_data["create_status_result"])
        self.assertContains(response,
                            _('Status created'))

    def test_status_update(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        status = Status.objects.get(name=self.test_data['update_status'])
        client.post(f'/statuses/{status.id}/update/',
                    self.test_data['update_status_data'])
        response = client.get('/statuses/')
        self.assertContains(response, self.test_data['update_status_result'])
        self.assertContains(response, _('Status changed'))

    def test_status_delete(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        status = Status.objects.get(name=self.test_data['delete_status'])
        client.post(f'/statuses/{status.id}/delete/',
                    self.test_data['delete_status_data'])
        response = client.get('/statuses/')
        self.assertNotContains(response, self.test_data['delete_status'])
        self.assertContains(response, _('Status deleted'))

    def test_delete_used_status(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        status = Status.objects.get(name=self.test_data['used_status'])
        client.post(f'/statuses/{status.id}/delete/',
                    self.test_data['delete_used_status_data'])
        response = client.get('/statuses/')
        self.assertContains(response, self.test_data['used_status'])
        self.assertContains(response, _("Can't delete status"))
