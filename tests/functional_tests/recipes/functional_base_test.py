from django.test import LiveServerTestCase
from utils.browser import make_browser


class RecipeFunctionalBaseTest(LiveServerTestCase):
    def setUp(self):
        self.browser = make_browser('--headless')
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
