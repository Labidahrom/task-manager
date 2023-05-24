from django.test import Client, TestCase
from task_manager.labels.models import Label
from django.utils.translation import gettext as _
from task_manager.tests import get_test_data


class LabelTestCase(TestCase):
    fixtures = ['task_manager/fixtures/database.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = get_test_data()

    def test_label_create(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        client.post('/labels/create/',
                    self.test_data['create_label_data'])
        response = client.get('/labels/')
        self.assertContains(response,
                            self.test_data["create_label_result"])
        self.assertContains(response,
                            _('Label created'))

    def test_label_update(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        label = Label.objects.get(name=self.test_data['update_label'])
        client.post(f'/labels/{label.id}/update/',
                    self.test_data['update_label_data'])
        response = client.get('/labels/')
        self.assertContains(response, self.test_data['update_label_result'])
        self.assertContains(response, _('Label changed'))

    def test_label_delete(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        label = Label.objects.get(name=self.test_data['delete_label'])
        client.post(f'/labels/{label.id}/delete/',
                    self.test_data['delete_label_data'])
        response = client.get('/labels/')
        self.assertNotContains(response, self.test_data['delete_label'])
        self.assertContains(response, _('Label deleted'))

    def test_delete_used_label(self):
        client = Client()
        client.post('/login/',
                    self.test_data['login_data'])
        label = Label.objects.get(name=self.test_data['used_label'])
        client.post(f'/labels/{label.id}/delete/',
                    self.test_data['delete_used_label_data'])
        response = client.get('/labels/')
        self.assertContains(response, self.test_data['used_label'])
        self.assertContains(response, _("Can't delete label"))
