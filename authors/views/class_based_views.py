from django.shortcuts import redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.models import User
from authors.forms import RegisterForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from recipes.models import Recipe
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from authors.models import Profile


class AuthorRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'authors/pages/register.html'
    success_url = reverse_lazy('authors:author_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Register'
        action = reverse('authors:author_register')

        context['title'] = title
        context['action'] = action

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if response:
            messages.success(self.request, 'User successfully registered!')

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if response:
            messages.error(self.request, 'Correct the form!')

        return response


class AuthorLoginView(LoginView):
    model = User
    # form_class = LoginForm
    template_name = 'authors/pages/login.html'
    next_page = reverse_lazy('authors:author_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Login'
        action = reverse('authors:author_login')

        context['title'] = title
        context['action'] = action

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if response:
            messages.success(self.request, 'User successfully logged in!')

        # return redirect('authors:author_dashboard')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if response:
            messages.error(self.request, 'Invalid login or password')

        return response


class AuthorLogoutView(LogoutView):
    model = User
    # next_page = reverse_lazy('recipes:recipe_list')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect('authors:author_login')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if request.POST.get('username') != request.user.username:
            return redirect('authors:author_login')

        logout(request)
        return redirect('recipes:recipe_list')


class AuthorDashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'authors/pages/dashboard.html'
    login_url = 'authors:author_login'

    def get_queryset(self):
        queryset = super().get_queryset()

        author_pk = self.request.user.pk
        queryset = queryset.filter(
            author__pk=author_pk,
            is_published=False,
        ).order_by('-pk')

        queryset = queryset.values(
            'pk',
            'title',
        )

        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        author_recipes = self.get_queryset()
        title = f'Dashboard - {self.request.user.first_name}'

        context["recipes"] = author_recipes
        context["title"] = title

        return context


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_pk = context.get('pk')
        profile = get_object_or_404(
            Profile.objects.filter(
                pk=profile_pk
            ).select_related('author'), pk=profile_pk
        )
        return self.render_to_response(
            {
                **context,
                'profile': profile,
            }
        )
