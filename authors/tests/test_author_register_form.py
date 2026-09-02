from unittest import TestCase
from django.forms import ValidationError
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse
from django.contrib.auth.models import User


class AuthorRegisterForm(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: Maria'),
        ('last_name', 'Ex.: da Silva'),
        ('email', 'Ex.: maria@dasilva.com'),
        ('username', 'mariadasilva'),
        ('password', 'Digite sua senha'),
        ('password2', 'Repita sua senha'),
    ])
    def test_fields_placeholders_are_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'Endereço de email'),
        ('username', 'Usuário'),
        ('password', 'Senha'),
        ('password2', 'Confirmação de Senha'),
    ])
    def test_fields_labels_are_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.label
        self.assertEqual(current_placeholder, placeholder)


class AuthorRegisterFormintegrationTest(DjangoTestCase):
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

    def make_user(self):
        del self.form_data['password2']
        user = User.objects.create_user(**self.form_data)
        return user

    @parameterized.expand([
        ('username', 'O campo Usuário não pode estar em branco'),
        ('first_name', 'O campo Nome não pode estar em branco'),
        ('last_name', 'O campo Sobrenome não pode estar em branco'),
        ('email', 'O campo Email não pode estar em branco'),
        ('password', 'Este campo é obrigatório'),
        ('password2', 'Este campo é obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:author_register')
        response = self.client.post(url, data=self.form_data)

        self.assertIn(msg, response.content.decode('utf-8'))

    @parameterized.expand([
        # ('username', 'Este campo é obrigatório'),
        ('first_name', 'O campo Nome deve conter pelo menos 3 caracteres'),
        ('last_name', 'O campo Sobrenome deve conter pelo menos 3 caracteres'),
        ('email', 'Informe um endereço de email válido.'),
        # ('password', 'Este campo é obrigatório'),
        # ('password2', 'Este campo é obrigatório'),
    ])
    def test_fields_min_length_raise_error(self, field, msg):
        self.form_data[field] = 'a' * 2 if field != 'email' else 'a@a'
        url = reverse('authors:author_register')
        response = self.client.post(url, data=self.form_data)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertRaises(ValidationError)

    def test_form_valid_save_correctly(self):
        msg = 'Usuário cadastrado com sucesso!'
        url = reverse('authors:author_register')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_method_get_load_empty_form_correctly(self):
        msg = 'Cadastre-se'
        url = reverse('authors:author_register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_trying_create_user_with_email_existing_raise_validation_error(self):
        msg = 'Já existe um usuário cadastrado com este email.'
        url = reverse('authors:author_register')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertRaises(ValidationError)

    def test_author_created_can_login(self):
        url = reverse('authors:author_register')
        self.client.post(url, data=self.form_data)

        user_login = self.client.login(
            username=self.form_data['username'],
            password=self.form_data['password']
        )

        self.assertEqual(user_login, True)
