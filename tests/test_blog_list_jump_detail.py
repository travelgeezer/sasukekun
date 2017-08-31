from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from blog.models import Blog


class BlogListTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        self.user = User.objects.create_user('geezer.', '', 'geezer.')
        super(BlogListTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(BlogListTestCase, self).tearDown()

    def test_should_goto_blog_detail_from_blog_list(self):
        Blog.objects.create(title='hello', author=self.user,
                            slug='this_is_a_test', body='This is a test',
                            posted=datetime.now)
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/blog/')
        )
        self.selenium.find_element_by_link_text('hello').click()

        self.assertIn('This is a test',
                      self.selenium.page_source)
