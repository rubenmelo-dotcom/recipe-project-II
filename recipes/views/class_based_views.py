from django.views import View
from recipes.forms import RecipeForm
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http.response import Http404
from recipes.models import Recipe
from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
import os
from django.core.paginator import Paginator
from django.db.models import Q  # type: ignore
from tag.models import Tag


PER_PAGE = os.getenv('PER_PAGE', 9)


class RecipeListViewBase(ListView):
    model = Recipe
    # queryset = None
    context_object_name = 'page_obj'
    ordering = '-id'
    # allow_empty = True
    paginate_by = None
    # paginate_orphans = 0
    # paginator_class = ...
    # page_kwarg = 'page'
    # template_name = ...

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        queryset = queryset.select_related('author', 'category')

        queryset = queryset.defer(
            'slug',
            'preparation_steps',
            'preparation_steps_is_html',
            'updated_at',
            'is_published',
            'is_published',
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)

        recipes = self.get_queryset()
        paginator = Paginator(recipes, PER_PAGE)
        page_number = self.request.GET.get('page', '')
        page_obj = paginator.get_page(page_number)

        context['recipes'] = recipes
        context['page_obj'] = page_obj

        return context


class RecipeHomeListView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)

        title = 'Recipes - Home'

        context['title'] = title

        return context


class RecipeSearchListView(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        search = self.request.GET.get('search', '').strip()
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(
                Q(title__icontains=search) |  # noqa: W504
                Q(description__icontains=search)
            )
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)

        search = self.request.GET.get('search').strip()
        title = f'Recipes - Search: {search}'

        context['search'] = search
        context['title'] = title

        return context


class RecipeCategoryListView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def get_queryset(self):
        cat_pk = self.kwargs.get('cat_pk')
        queryset = super().get_queryset()
        queryset = get_list_or_404(
            queryset.filter(
                category__pk=cat_pk,
            )
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        recipes = self.get_queryset()
        title = f'Recipes - Categoria {recipes[0].category.name}'

        context['title'] = title

        return context


class RecipeCreateView(LoginRequiredMixin, View):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/pages/recipe_create.html'
    success_url = reverse_lazy('authors:author_dashboard')
    login_url = 'authors:author_login'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        form = RecipeForm(
        )

        context = {
            'form': form,
            'title': f'Create Recipe - {request.user.first_name}',
            'action': reverse('recipes:recipe_create'),
        }
        return render(
            request,
            'recipes/pages/recipe_create.html',
            context
        )

    def post(self, request, *args, **kwargs):
        form = RecipeForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
        )
        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = self.request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            form.save()

            messages.success(self.request, 'Recipe successfully created!')

            return redirect('authors:author_dashboard')

        return render(
            request,
            self.template_name,
            context={'form': form}
        )


    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = self.form
    #     context["title"] = f'Create Recipe - {self.request.user.first_name}'
    #     context["action"] = reverse('recipes:recipe_create')
    #     return context


class RecipeUpdateView(LoginRequiredMixin, View):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/pages/recipe_update.html'
    success_url = reverse_lazy('authors:author_dashboard')
    login_url = 'authors:author_login'
    redirect_field_name = 'next'

    def get_recipe(self, *args, **kwargs):
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
        else:
            pk = self.request.POST.get('pk')
        recipe = get_object_or_404(
            Recipe.objects.filter(
                pk=pk,
                is_published=False,
                author=self.request.user,
            )
        )
        return recipe

    def get_form_post(self):
        recipe = self.get_recipe()
        form = RecipeForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=recipe,
        )
        return form

    def get(self, *args, **kwargs):
        recipe = self.get_recipe()

        form = self.get_form_post()

        context = {
            'recipe': recipe,
            'form': form,
            'title': f'Update - {recipe.title}',
            'action': reverse('recipes:recipe_update', args=(recipe.pk,)),
        }
        return render(
            self.request,
            'recipes/pages/recipe_update.html',
            context
        )

    def post(self, *args, **kwargs):
        recipe = self.get_recipe()
        form = self.get_form_post()
        if form.is_valid():
            form.save(commit=False)

            recipe.author = self.request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            form.save()

        messages.success(self.request, 'Recipe successfully updated!')

        return redirect('authors:author_dashboard')


class RecipeDeleteView(RecipeUpdateView):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe()

        if not recipe:
            raise Http404

        recipe.delete()
        messages.success(self.request, 'Deleted successfully')
        return redirect('authors:author_dashboard')


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_queryset().first()
        title = f'Recipe - {recipe.title}'

        context['title'] = title

        return context


class RecipeTagListView(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            tags__slug=self.kwargs.get('slug', '')
        )
        queryset = queryset.prefetch_related('tags')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()
        if not title:
            title = 'No recipes found'

        context['title'] = f'Tag - {title}'

        return context
