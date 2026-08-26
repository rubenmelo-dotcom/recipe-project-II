from django.shortcuts import render
from utils.recipes.factory import make_recipe
from recipes.models import Recipe, Category    # noqa: F401
from django.db.models import Q  # type: ignore
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
import os

PER_PAGE = os.getenv('PER_PAGE', 9)


def home_list_view(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    paginator = Paginator(recipes, PER_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    title = 'Recipes - Home'

    context = {
        'recipes': recipes,
        'title': title,
        'page_obj': page_obj,
    }
    return render(
        request,
        'recipes/pages/home.html',
        context,
    )


def recipe_search_view(request):
    search = request.GET.get('search').strip()
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search) |  # noqa: W504
            Q(description__icontains=search)
        ),
        is_published=True
    ).order_by('-id')
    paginator = Paginator(recipes, PER_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj.paginator.num_pages)
    print(recipes)
    title = f'Recipes - Search: {search}'

    context = {
        'recipes': recipes,
        'title': title,
        'search': search,
        'page_obj': page_obj,
    }
    return render(
        request,
        'recipes/pages/search.html',
        context
    )


def category_list_view(request, cat_pk):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__pk=cat_pk,
            is_published=True,
        ).order_by('-id')
    )
    paginator = Paginator(recipes, PER_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': recipes,
        'title': f'Recipes - Categoria {recipes[0].category.name}',
        'page_obj': page_obj,
    }
    return render(
        request,
        'recipes/pages/home.html',
        context
    )


def recipe_detail_view(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.filter(
            pk=pk,
            is_published=True,
        )
    )
    fake_recipe = make_recipe()  # noqa: F841
    context = {
        'recipe': recipe,
        'title': f'Recipe - {recipe.title}'
    }
    return render(
        request,
        'recipes/pages/recipe.html',
        context
    )
