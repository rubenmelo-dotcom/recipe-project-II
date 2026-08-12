from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:recipe_list')

        self.assertEqual(url, '/')

    def test_recipe_category_list_url_is_correct(self):
        url = reverse('recipes:category_list', kwargs={'cat_pk': 1})

        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe_detail', kwargs={'pk': 1})

        self.assertEqual(url, '/recipes/1/')
