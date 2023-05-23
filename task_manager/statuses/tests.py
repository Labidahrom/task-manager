from django.test import Client, TestCase
from task_manager.statuses.models import Status
from task_manager.tests import get_test_data
from django.utils.translation import gettext as _


TEST_DATA = get_test_data()


class StatusTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def test_status_create(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        client.post('/statuses/create/',
                    TEST_DATA['create_status_data'])
        response = client.get('/statuses/')
        self.assertContains(response,
                            TEST_DATA["create_status_result"])
        self.assertContains(response,
                            _('Status created'))

    def test_status_update(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        status = Status.objects.get(name=TEST_DATA['update_status'])
        client.post(f'/statuses/{status.id}/update/',
                    TEST_DATA['update_status_data'])
        response = client.get('/statuses/')
        self.assertContains(response, TEST_DATA['update_status_result'])
        self.assertContains(response, _('Status changed'))

    def test_status_delete(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        status = Status.objects.get(name=TEST_DATA['delete_status'])
        client.post(f'/statuses/{status.id}/delete/',
                    TEST_DATA['delete_status_data'])
        response = client.get('/statuses/')
        self.assertNotContains(response, TEST_DATA['delete_status'])
        self.assertContains(response, _('Status deleted'))

    def test_delete_used_status(self):
        client = Client()
        client.post('/login/',
                    TEST_DATA['login_data'])
        status = Status.objects.get(name=TEST_DATA['used_status'])
        client.post(f'/statuses/{status.id}/delete/',
                    TEST_DATA['delete_used_status_data'])
        response = client.get('/statuses/')
        self.assertContains(response, TEST_DATA['used_status'])
        self.assertContains(response, _("Can't delete status"))
