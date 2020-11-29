
import os
import django
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from metadb.views import MainView

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geocore.settings.development')
django.setup()

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/en-us/metadb/')
        self.assertEqual(found.func.view_class, MainView)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        response = MainView.as_view()(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>MetaDB administrative console</title>', html)
