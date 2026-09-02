from django.shortcuts import redirect, render
from authors.forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_test(request):
    if request.POST:
        form = RegisterForm(request.POST)
        context = {
            'form': form,
            'title': 'Register'
        }

        if not form.is_valid():
            messages.error(request, 'Corrija o formulário')

            return render(
                request,
                'authors/pages/register.html',
                context,
            )

        else:
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')

            return redirect('authors:author_login')

    else:
        form = RegisterForm()

    context = {
        'form': form,
        'title': 'Register'
    }
    return render(
        request,
        'authors/pages/register.html',
        context,
    )


def login_test(request):
    if request.POST:
        form = LoginForm(request.POST)
        context = {
            'form': form,
            'title': 'Login'
        }

        if not form.is_valid():
            messages.error(request, 'Corrija o formulário!')

            return redirect('authors:author_login')

        else:
            authenticate_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', '')
            )

            if authenticate_user is not None:
                login(request, authenticate_user)

                messages.success(request, 'Usuário logado com sucesso!')
                return redirect('recipes:recipe_list')
            else:
                messages.error(request, 'Login ou senha inválidos')

                return redirect('authors:author_login')

    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Login'
    }
    return render(
        request,
        'authors/pages/login.html',
        context,
    )


@login_required(login_url='authors:author_login')
def logout_test(request):
    if not request.POST:
        return redirect('authors:author_login')

    if request.POST.get('username') != request.user.username:
        return redirect('authors:author_login')

    logout(request)
    return redirect('recipes:recipe_list')
