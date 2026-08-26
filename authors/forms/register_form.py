from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
import re


def password_validation(password):
    validation = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[A-Z]){8,}$')
    if not re.match(validation, password):
        return False
    return True


def add_attr(field, attr_name, attr_new_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_value}'.strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Ex.: Maria')
        add_placeholder(self.fields['last_name'], 'Ex.: da Silva')
        add_placeholder(self.fields['email'], 'Ex.: maria@dasilva.com')
        add_placeholder(self.fields['username'], 'mariadasilva')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='Senha',
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='Confirmação de Senha',
    )

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password',
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()

        if not first_name:
            raise ValidationError(
                'O campo Nome não pode estar em branco',
                code='invalid',
            )
        if len(first_name) < 3:
            raise ValidationError(
                'O campo Nome deve conter pelo menos 3 caracteres',
                code='invalid',
            )
        return first_name

    def clean_last_name(self):
        last_name = (self.cleaned_data.get('last_name') or '').strip()
        first_name = (self.cleaned_data.get('first_name') or '').strip()

        if not first_name or not last_name:
            return last_name

        if not last_name:
            raise ValidationError(
                'O campo Sobrenome não pode estar em branco',
                code='invalid',
            )
        if len(last_name) < 3:
            raise ValidationError(
                'O campo Sobrenome deve conter pelo menos 3 caracteres',
                code='invalid',
            )

        queryset = User.objects.filter(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                'Já existe um usuário cadastrado com este nome e sobrenome.',
                code='invalid',
            )
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if not email:
            raise ValidationError(
                'O campo Email não pode estar em branco',
                code='invalid',
            )
        if len(email) < 4:
            raise ValidationError(
                'O campo Email deve conter pelo menos 3 caracteres',
                code='invalid',
            )
        queryset = User.objects.filter(
            email__iexact=email,
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                'Já existe um usuário cadastrado com este email.',
                code='invalid',
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()

        if not username:
            raise ValidationError(
                'O campo Username não pode estar em branco',
                code='invalid',
            )
        if len(username) < 3:
            raise ValidationError(
                'O campo Username deve conter pelo menos 3 caracteres',
                code='invalid',
            )
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise ValidationError(
                'A confirmação de senha é diferente da senha',
                code='invalid',
            )

        # if not password_validation(password2):
        #     raise ValidationError(
        #         'A senha é muito fraca. Crie uma senha que lute como Mike Tayson',
        #         code='invalid',
        #     )
        return password2
