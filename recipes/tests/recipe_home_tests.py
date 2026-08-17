from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.tests.recipe_base_test import RecipeBaseTest


class RecipeDetailTest(RecipeBaseTest):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:recipe_list')

        self.assertEqual(url, '/')

    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse('recipes:recipe_list'))

        self.assertIs(view.func, views.home_list_view)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        url = reverse('recipes:recipe_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        url = reverse('recipes:recipe_list')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_not_found_recipes_witout_published_recipe(self):
        url = reverse('recipes:recipe_list')
        response = self.client.get(url)

        self.assertIn(
            'Nenhum receita publicada. Volte mais tarde.',
            response.content.decode(
                'utf-8'
            )
        )

    def test_recipe_home_template_loads_recipes(self):
        recipe = self._make_recipe()
        url = reverse('recipes:recipe_list')
        response = self.client.get(url)
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 1)
        self.assertEqual(recipes_in_context[0].pk, recipe.pk)
        self.assertContains(response, recipe.title)

    def test_recipe_home_template_dont_loads_recipes_not_published(self):
        recipe = self._make_recipe(is_published=False)
        url = reverse('recipes:recipe_list')
        response = self.client.get(url)
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 0)
        self.assertNotContains(response, recipe.title)

    def test_recipe_home_search_template_loads_recipes_sought_after(self):
        recipe = self._make_recipe(title='sought_after_title')
        url = reverse('recipes:recipe_list')
        response = self.client.get(url, data={'search': 'sought_a'})
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 1)
        self.assertContains(response, recipe.title)

