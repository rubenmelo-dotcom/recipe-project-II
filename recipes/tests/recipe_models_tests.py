from recipes.tests.recipe_base_test import RecipeBaseTest
from django.core.exceptions import ValidationError
from recipes.models import Recipe


class RecipeModeltest(RecipeBaseTest):
    def setUp(self):
        self.recipe = self._make_recipe()
        return super().setUp()

    def make_recipe_default(self):
        recipe = Recipe(
            title='Recipe Title',
            description="Recipe Description",
            slug='recipe-slug',
            preparation_time=1,
            servings=1,
            preparation_steps='Recipe Preparation Steps',
            cover=self._make_test_image(),
            category=self._make_category(name='Recipe Category'),
            author=self._make_author(username='another_username')
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_fields_max_length(self):
        fields = [
            ('title', 65),
            ('description', 165),
        ]

        for field, max_length in fields:
            with self.subTest(field=field, max_length=max_length):
                setattr(self.recipe, field, 'A' * (max_length + 1))
                with self.assertRaises(ValidationError):
                    self.recipe.full_clean()

    def test_category_fields_max_length(self):
        category = self._make_category(name='A' * 66)

        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_recipe_fields_values_default(self):
        recipe = self.make_recipe_default()

        self.assertEqual(recipe.preparation_time_unit, 'Minutes')
        self.assertEqual(recipe.servings_unit, 'Pieces')
        self.assertFalse(recipe.preparation_steps_is_html)
        self.assertFalse(recipe.is_published)

    def test_recipe_str_method_returns_correctly(self):

        self.assertEqual(self.recipe.__str__(), 'test_title')
        self.assertEqual(self.recipe.category.__str__(), 'test_category')
