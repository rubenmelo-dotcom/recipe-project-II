from django.shortcuts import redirect, render
from authors.forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe


def register_test(request):
    if request.POST:
        form = RegisterForm(request.POST)
        context = {
            'form': form,
            'title': 'Register',
            'action': reverse('authors:author_register'),
        }

        if not form.is_valid():
            messages.error(request, 'Correct the form!')

            return render(
                request,
                'authors/pages/register.html',
                context,
            )

        else:
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, 'User successfully registered!')

            return redirect('authors:author_login')

    else:
        form = RegisterForm()

    context = {
        'form': form,
        'title': 'Register',
        'action': reverse('authors:author_register'),
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
            'title': 'Login',
            'action': reverse('authors:author_login'),
        }

        if not form.is_valid():
            messages.error(request, 'Correct the form!')

            return redirect('authors:author_login')

        else:
            authenticate_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', '')
            )

            if authenticate_user is not None:
                login(request, authenticate_user)

                messages.success(request, 'User successfully logged in!')
                return redirect('authors:author_dashboard')
            else:
                messages.error(request, 'Invalid login or password')

                return redirect('authors:author_login')

    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Login',
        'action': reverse('authors:author_login'),
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


@login_required(login_url='authors:author_login')
def dashboard_test(request):
    author_pk = request.user.pk
    author_recipes = Recipe.objects.filter(
        author__pk=author_pk,
        is_published=False,
    ).order_by('-pk')

    context = {
        'recipes': author_recipes,
        'title': f'Dashboard - {request.user.first_name}',
    }

    return render(
        request,
        'authors/pages/dashboard.html',
        context
    )


# @login_required(login_url='authors:author_login')
# def dashboard_test(request):
#     context = {
#         'title': f'Dashboard - {request.user.first_name}',
#     }

#     return render(
#         request,
#         'authors/pages/dashboard.html',
#         context
#     )
