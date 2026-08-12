from django.urls import reverse, resolve
from recipes import views
from recipes.tests.recipe_base_test import RecipeBaseTest


class RecipeViewsTest(RecipeBaseTest):
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




    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe_detail', kwargs={'pk': 1}))

        self.assertIs(view.func, views.recipe_detail)

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

    def test_recipe_home_template_dont_loads_recipe_not_published(self):
        recipe = self._make_recipe(is_published=False)
        url = reverse('recipes:recipe_detail', kwargs={'pk': recipe.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)





    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse('recipes:category_list', kwargs={'cat_pk': 1}))

        self.assertIs(view.func, views.category_list_view)

    def test_recipe_category_view_returns_status_code_200_ok(self):
        recipe = self._make_recipe()

        url = reverse('recipes:category_list', kwargs={'cat_pk': recipe.category.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_loads_correct_template(self):
        recipe = self._make_recipe()

        url = reverse('recipes:category_list', kwargs={'cat_pk': recipe.category.pk})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_category_view_returns_status_code_404_with_recipe_non_existent(self):  # noqa: E501
        url = reverse('recipes:category_list', kwargs={'cat_pk': 1, })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_loads_recipes(self):
        recipe = self._make_recipe()

        url = reverse('recipes:category_list', kwargs={'cat_pk': recipe.category.pk})
        response = self.client.get(url)
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 1)
        self.assertEqual(recipes_in_context[0].pk, recipe.pk)
        self.assertContains(response, recipe.title)

    def test_recipe_category_template_dont_loads_recipes_not_published(self):
        recipe_1 = self._make_recipe(title='not_shoud_be_found', is_published=False)
        recipe_2 = self._make_recipe(
            title='shoud_be_found',
            author_data={
                'first_name': 'another_first_name',
                'last_name': 'another_last_name',
                'username': 'another_username',
                'email': 'another@email.com',
            }
        )
        recipe_2.category = recipe_1.category
        recipe_2.save()

        url = reverse('recipes:category_list', kwargs={'cat_pk': recipe_1.category.pk})
        response = self.client.get(url)
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 1)
        self.assertNotContains(response, recipe_1.title)
        self.assertContains(response, recipe_2.title)
