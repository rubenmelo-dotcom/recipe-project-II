from unittest.mock import patch
from django.urls import reverse, resolve
from recipes import views
from recipes.tests.recipe_base_test import RecipeBaseTest


class RecipeSearchTest(RecipeBaseTest):
    # Trocar os nomes e refazer os testes para search
    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:recipe_search')

        self.assertEqual(url, '/recipes/search/')

    def test_recipe_search_view_is_correct(self):
        view = resolve(reverse('recipes:recipe_search'))

        self.assertIs(view.func, views.recipe_search_view)

    def test_recipe_search_view_returns_status_code_200_ok(self):
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, data={'search': 'search_term'})

        self.assertEqual(response.status_code, 200)

    def test_recipe_search_view_loads_correct_template(self):
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, data={'search': 'search_term'})

        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_template_shows_not_found_recipes_witout_published_recipe(self):
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, data={'search': 'search_term'})

        self.assertIn(
            'Nenhum receita encontrada.',
            response.content.decode(
                'utf-8'
            )
        )

    def test_recipe_search_template_loads_recipes(self):
        recipe = self._make_recipe()
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, data={'search': recipe.title[:4]})
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 1)
        self.assertEqual(recipes_in_context[0].pk, recipe.pk)
        self.assertContains(response, recipe.title)

    def test_recipe_search_template_dont_loads_recipes_not_published(self):
        recipe = self._make_recipe(is_published=False)
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, data={'search': recipe.title[:4]})
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 0)
        self.assertNotContains(response, recipe.title)

    def test_recipe_home_search_template_loads_recipes_sought_after(self):
        recipe_1 = self._make_recipe(title='Cuscuz para café da manhã44')
        recipe_2 = self._make_recipe(
            title='Sanduíche natural café da manhã44',
            author_data={'username': 'another_username'})
        url = reverse('recipes:recipe_search')
        response = self.client.get(url, data={'search': recipe_1.title[:4]})
        recipes_in_context = response.context['recipes']

        self.assertIn('recipes', response.context)
        self.assertEqual(len(recipes_in_context), 1)
        self.assertContains(response, recipe_1.title)
        self.assertNotContains(response, recipe_2.title)

        response_2 = self.client.get(url, data={'search': recipe_2.title[:4]})
        recipes_in_context_2 = response_2.context['recipes']

        self.assertIn('recipes', response_2.context)
        self.assertEqual(len(recipes_in_context_2), 1)
        self.assertContains(response_2, recipe_2.title)
        self.assertNotContains(response_2, recipe_1.title)

        response_3 = self.client.get(url, data={'search': recipe_1.title[12:-1]})
        recipes_in_context_3 = response_3.context['recipes']

        self.assertIn('recipes', response_3.context)
        self.assertEqual(len(recipes_in_context_3), 2)
        self.assertContains(response_3, recipe_1.title)
        self.assertContains(response_3, recipe_2.title)

    @patch('recipes.views.PER_PAGE', new=3)    
    def test_recipe_search_pagination_loads_correctly_qtd_pages(self):
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
    def test_recipe_search_pagination_is_not_displayed_with_less_tha_two_pages_of_content(self):
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
