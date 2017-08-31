from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from blog.models import Blog


class HomePgaeTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        self.user = User.objects.create_user('geezer.', '', 'geezer.')
        super(HomePgaeTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(HomePgaeTestCase, self).tearDown()

    def test_should_goto_blog_page_from_homepage(self):
        Blog.objects.create(title='hello', author=self.user,
                            slug='this_is_a_test', body='This is a test',
                            posted=datetime.now)
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/")
        )
        self.selenium.find_element_by_link_text('博客').click()

        self.assertIn('This is a test',
                      self.selenium.page_source)
