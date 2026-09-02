import time
from tests.functional_tests.authors.base_test import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from unittest.mock import patch
from recipes.tests.recipe_base_test import RecipeMixin


@pytest.mark.functional_test
class AuthorLoginTest(AuthorsBaseTest, RecipeMixin):
    def get_by_name(self, web_element, name):
        return web_element.find_element(
            By.NAME,
            name
        )

    def fill_form_fields(self, web_element):
        fields = web_element.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def test_the_test(self):
        self.browser.get(f'{self.live_server_url}/authors/login')

        form_title = self.browser.find_element(
            By.TAG_NAME, 'h2'
        )

        self.assertIn('Faça Login', form_title.text)

    def test_validation_empty_fields_form(self):
        self.browser.get(f'{self.live_server_url}/authors/login')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.fill_form_fields(form)

        form.submit()

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('Corrija o formulário!', body.text)

    def test_trying_login_with_invalid_data(self):
        author = self._make_author(
            first_name='first_name',
            last_name='last_name',
            username='username',
            email='email@email.com',
            password='P@ssW0rd'
        )
        self.browser.get(f'{self.live_server_url}/authors/login')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.get_by_name(form, 'username').send_keys('username_inc')
        self.get_by_name(form, 'password').send_keys('P@ssW0rd_inc')

        form.submit()

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('Login ou senha inválidos', body.text)

    def test_author_login_success(self):
        author = self._make_author(
            first_name='first_name',
            last_name='last_name',
            username='username',
            email='email@email.com',
            password='P@ssW0rd'
        )
        self.browser.get(f'{self.live_server_url}/authors/login')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.get_by_name(form, 'username').send_keys(author.username)
        self.get_by_name(form, 'password').send_keys('P@ssW0rd')

        form.submit()

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('Usuário logado com sucesso!', body.text)
        self.assertIn(f'Logado com {author.first_name}.', body.text)
