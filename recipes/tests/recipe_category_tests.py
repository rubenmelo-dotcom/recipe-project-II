from unittest.mock import patch
from django.urls import reverse, resolve
from recipes import views
from recipes.tests.recipe_base_test import RecipeBaseTest


class RecipeCategoryTest(RecipeBaseTest):
    def test_recipe_category_list_url_is_correct(self):
        url = reverse('recipes:category_list', kwargs={'cat_pk': 1})

        self.assertEqual(url, '/recipes/category/1/')

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

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_category_pagination_loads_correctly_qtd_pages(self):
        recipes = self._make_recipe_at_scale(4)

        url = reverse('recipes:recipe_list')
        response = self.client.get(url)
        recipes_in_context = response.context['recipes']
        recipes_in_page = response.context['page_obj']
        paginator = recipes_in_page.paginator

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 4)
        self.assertIn('Page 1 of 2.', response.content.decode('utf-8'))
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 1)
        self.assertEqual(paginator.num_pages, 2)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_category_pagination_is_not_displayed_with_less_tha_two_pages_of_content(self):
        recipes = self._make_recipe_at_scale(2)

        url = reverse('recipes:recipe_list')
        response = self.client.get(url)
        recipes_in_context = response.context['recipes']
        recipes_in_page = response.context['page_obj']
        paginator = recipes_in_page.paginator

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 2)
        self.assertNotIn('Page 1 of 2.', response.content.decode('utf-8'))
        self.assertEqual(len(paginator.get_page(1)), 2)
        self.assertEqual(paginator.num_pages, 1)

    def test_recipe_category_str_method_restur_name_correctly(self):
        recipe = self._make_recipe()
        category = recipe.category

        url = reverse('recipes:category_list', kwargs={'cat_pk': category.pk})
        response = self.client.get(url)

        self.assertEqual(str(category), category.name)
