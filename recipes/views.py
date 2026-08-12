from django.shortcuts import render  # type: ignore
from utils.recipes.factory import make_recipe
from recipes.models import Recipe, Category    # noqa: F401
from django.db.models import Q  # type: ignore
from django.shortcuts import get_list_or_404, get_object_or_404


def home_list_view(request):
    search = request.GET.get('search')
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    if search:
        recipes = recipes.filter(
            Q(title__icontains=search) |  # noqa: W504
            Q(description__icontains=search)
        )

    fake_recipes = [make_recipe() for _ in range(9)]  # noqa: F841
    title = 'Recipes - Home' if not search else f'Recipes - {search}'

    context = {
        'recipes': recipes,
        'title': title,
    }
    return render(
        request,
        'recipes/pages/home.html',
        context
    )


def category_list_view(request, cat_pk):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__pk=cat_pk,
            is_published=True,
        ).order_by('-id')
    )
    fake_recipes = [make_recipe() for _ in range(9)]  # noqa: F841
    context = {
        'recipes': recipes,
        'title': f'Recipes - Categoria {recipes[0].category.name}'
    }
    return render(
        request,
        'recipes/pages/home.html',
        context
    )


def recipe_detail(request, pk):
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
