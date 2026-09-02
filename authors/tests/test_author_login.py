from django.test import TestCase
from django.forms import ValidationError
from parameterized import parameterized
from django.urls import reverse
from django.contrib.auth.models import User
from authors.tests.test_author_register_form import AuthorRegisterFormintegrationTest
from django.contrib.auth import login, authenticate


class TestsAuthorLogin(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssW0rd1',
            'password2': 'Str0ngP@ssW0rd1',
        }
        return super().setUp()

    def make_author(self):
        data = self.form_data
        del data['password2']

        user = User.objects.create_user(**data)

        return user

    def test_login_author_success(self):
        author = self.make_author()
        url = reverse('authors:author_login')
        response = self.client.post(
            url,
            data={
                'username': 'username',
                'password': 'Str0ngP@ssW0rd1'
            },
            follow=True
        )

        # self.assertNotEqual(authenticate(author), None)
        self.assertIn('Usuário logado com sucesso!', response.content.decode('utf-8'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_author_failed(self):
        author = self.make_author()
        url = reverse('authors:author_login')
        response = self.client.post(
            url,
            data={
                'username': 'username',
                'password': 'Str0ngP@ssW0rd12'
            },
            follow=True
        )

        self.assertIn('Login ou senha inválidos', response.content.decode('utf-8'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_author_with_invalid_form(self):
        author = self.make_author()
        url = reverse('authors:author_login')
        response = self.client.post(
            url,
            data={
                'username': ' ',
                'password': 'Str0ngP@ssW0rd1'
            },
            follow=True
        )

        self.assertIn('Corrija o formulário', response.content.decode('utf-8'))
        self.assertRaises(ValidationError)

    def test_logout_author_success(self):
        author = self.make_author()
        login_url = reverse('authors:author_login')
        login_response = self.client.post(
            login_url,
            data={
                'username': 'username',
                'password': 'Str0ngP@ssW0rd1'
            },
            follow=True
        )

        self.assertIn('Usuário logado com sucesso!', login_response.content.decode('utf-8'))
        self.assertEqual(int(self.client.session['_auth_user_id']), author.pk)

        logout_url = reverse('authors:author_logout')
        logout_response = self.client.post(
            logout_url,
            data={'username': 'username'},
            follow=True
        )

        self.assertFalse(logout_response.context['user'].is_authenticated)

    def test_logout_author_failded(self):
        author = self.make_author()
        login_url = reverse('authors:author_login')
        login_response = self.client.post(
            login_url,
            data={
                'username': 'username',
                'password': 'Str0ngP@ssW0rd1'
            },
            follow=True
        )

        self.assertIn('Usuário logado com sucesso!', login_response.content.decode('utf-8'))
        self.assertEqual(int(self.client.session['_auth_user_id']), author.pk)

        logout_url = reverse('authors:author_logout')
        logout_response = self.client.post(
            logout_url,
            data={
                'username': 'wrong_username',
            },
            follow=True
        )

        self.assertTrue(logout_response.context['user'].is_authenticated)

        self.client.get(logout_url, follow=True)

        self.assertTrue(logout_response.context['user'].is_authenticated)
