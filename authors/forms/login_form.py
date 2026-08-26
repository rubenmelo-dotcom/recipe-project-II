from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Usuário'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='Senha',
    )
