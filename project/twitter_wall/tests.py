from django.test import TestCase
from django.test import Client


# Create your tests here.
class UrlTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_get_twitlist(self):
        response = self.client.get('/twit/list/')
        self.assertEqual(response.status_code, 200)
