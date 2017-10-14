from django.http import HttpRequest
from django.test import TestCase
from django.core.urlresolvers import resolve


# Create your tests here.

from homepage.views import index


class HomePageTset(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertIn(b' <title>sasukekun</title>',
                      response.content)
