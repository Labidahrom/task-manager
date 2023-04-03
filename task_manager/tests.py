from django.test import Client, TestCase

class SimpleTestCase(TestCase):
    def test_header(self):
        # create a client instance
        client = Client()

        # make a GET request to the inbox page
        response = client.get('/')

        # check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # check that the response contains the text "Welcome to your inbox"
        self.assertContains(response, "Менеджер задач")