from django.urls import reverse, resolve
from recipes import views
from recipes.tests.recipe_base_test import RecipeBaseTest


class RecipeDetailTest(RecipeBaseTest):
    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe_detail', kwargs={'pk': 1})

        self.assertEqual(url, '/recipes/1/')

    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe_detail', kwargs={'pk': 1}))

        self.assertIs(view.func, views.recipe_detail_view)

    def test_recipe_detail_view_returns_status_code_200_ok(self):
        recipe = self._make_recipe()

        url = reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_loads_correct_template(self):
        recipe = self._make_recipe()

        url = reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'recipes/pages/recipe.html')

    def test_recipe_detail_view_returns_status_code_404_with_recipe_non_existent(self):
        url = reverse('recipes:recipe_detail', kwargs={'pk': 1}, )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_loads_recipes(self):
        recipe = self._make_recipe()

        url = reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(url)
        recipes_in_context = response.context['recipe']

        self.assertIn('recipe', response.context)
        self.assertEqual(recipes_in_context, recipe)
        self.assertEqual(recipes_in_context.pk, recipe.pk)
        self.assertContains(response, recipe.title)

    def test_recipe_detail_template_dont_loads_recipe_not_published(self):
        recipe = self._make_recipe(is_published=False)
        url = reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
