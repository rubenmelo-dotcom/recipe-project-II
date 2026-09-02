from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_browser('--headless')
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def test_the_test(self):
        assert 1 == 1
