from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from blog.models import Blog


class BlogpostListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('geezer.', '', 'geezer.')

    def test_blog_list_page(self):
        Blog.objects.create(title='hello', author=self.user,
                            slug='this_is_a_test', body='This is a test',
                            posted=datetime.now)
        response = self.client.get('/blog/')
        self.assertIn(b'This is a test', response.content)

    def test_blog_detail_page(self):
        Blog.objects.create(title='hello', author=self.user,
                            slug='this_is_a_test', body='This is a test',
                            posted=datetime.now)
        response = self.client.get('/blog/this_is_a_test.html/')
        self.assertIn(b'This is a test', response.content)

    def test_not_found_blog(self):
        response = self.client.get('/blog/this_not_a_blog.html')
        self.assertEqual(404, response.status_code)
