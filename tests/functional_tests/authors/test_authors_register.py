import time
from tests.functional_tests.authors.base_test import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from unittest.mock import patch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthorRegisterTest(AuthorsBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_fields(self, web_element):
        fields = web_element.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def fill_form_fields_with_2_chars(self, web_element):
        fields = web_element.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def test_the_test(self):
        self.browser.get(f'{self.live_server_url}/authors/register')

        form_title = self.browser.find_element(
            By.TAG_NAME, 'h2'
        )

        self.assertIn('Cadastre-se', form_title.text)

    def test_validation_empty_fields_form(self):
        self.browser.get(f'{self.live_server_url}/authors/register')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.fill_form_fields(form)

        first_name = self.get_by_placeholder(form, 'Ex.: Maria')
        first_name.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                'Por favor corrija os erros no formulário!'
            )
        )

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('Por favor corrija os erros no formulário!', body.text)
        self.assertIn('O campo Nome não pode estar em branco', body.text)
        self.assertIn('O campo Sobrenome não pode estar em branco', body.text)
        self.assertIn('O campo Email não pode estar em branco', body.text)
        self.assertIn('O campo Usuário não pode estar em branco', body.text)

    def test_validation_min_length_first_name_field_form(self):
        self.browser.get(f'{self.live_server_url}/authors/register')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.fill_form_fields(form)

        # email_field = form.find_element(By.NAME, 'email')
        # email_field.send_keys('maria@email.com')

        first_name = self.get_by_placeholder(form, 'Ex.: Maria')
        first_name.send_keys('ab')
        first_name.send_keys(Keys.ENTER)

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('O campo Nome deve conter pelo menos 3 caracteres', body.text)

    def test_validation_min_length_username_field_form(self):
        self.browser.get(f'{self.live_server_url}/authors/register')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.fill_form_fields(form)

        username_field = form.find_element(By.NAME, 'username')
        username_field.send_keys('us')

        form.submit()

        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                'O campo Username deve conter pelo menos 3 caracteres'
            )
        )

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('O campo Username deve conter pelo menos 3 caracteres', body.text)

    def test_validation_min_length_email_field_form(self):
        self.browser.get(f'{self.live_server_url}/authors/register')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.fill_form_fields(form)

        email_field = form.find_element(By.NAME, 'email')
        email_field.send_keys('a@b')

        form.submit()

        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                'Corrija o formulário'
            )
        )

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('Informe um endereço de email válido.', body.text)

    def test_email_field_form_data_invalid(self):
        self.browser.get(f'{self.live_server_url}/authors/register')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.fill_form_fields(form)

        email_field = form.find_element(By.NAME, 'email')
        email_field.send_keys('maria@email')

        email_field.send_keys(Keys.ENTER)

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('Informe um endereço de email válido.', body.text)

    def test_password_field_form_with_different_values(self):
        self.browser.get(f'{self.live_server_url}/authors/register')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.fill_form_fields(form)

        password = form.find_element(By.NAME, 'password')
        password.send_keys('P@ssW0rd1')

        password2 = form.find_element(By.NAME, 'password2')
        password2.send_keys('P@ssW0rd')

        password2.send_keys(Keys.ENTER)

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('A confirmação de senha é diferente da senha', body.text)

    def test_register_author_success(self):
        self.browser.get(f'{self.live_server_url}/authors/register')
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[3]/form'
        )

        self.get_by_placeholder(form, 'Ex.: Maria').send_keys('Maria')
        self.get_by_placeholder(form, 'Ex.: da Silva').send_keys('da Silva')
        self.get_by_placeholder(form, 'Ex.: maria@dasilva.com').send_keys('maria@dasilva.com')
        self.get_by_placeholder(form, 'mariadasilva').send_keys('mariadasilva')
        self.get_by_placeholder(form, 'Digite sua senha').send_keys('P@ssW0rd')
        self.get_by_placeholder(form, 'Repita sua senha').send_keys('P@ssW0rd')
        form.submit()

        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, 'body'),
                'Usuário cadastrado com sucesso!'
            )
        )

        body = self.browser.find_element(By.TAG_NAME, 'body')

        # sleep(20)
        self.assertIn('Faça Login', body.text)
