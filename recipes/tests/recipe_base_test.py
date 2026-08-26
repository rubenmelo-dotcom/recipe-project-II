from django.test import TestCase
from recipes.models import Recipe, Category
from django.contrib.auth.models import User
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class RecipeBaseTest(TestCase):
    def _make_test_image(self):
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(file, 'jpeg')
        file.seek(0)

        return SimpleUploadedFile(
            name='test_image.jpg',
            content=file.read(),
            content_type='image/jpeg'
        )

    def _make_author(
            self,
            first_name='user',
            last_name='name',
            username='username',
            email='test@email.com',
            password='Recipe@200_Or_404'
    ):
        author = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        return author

    def _make_category(
            self,
            name='test_category'
    ):
        category = Category.objects.create(
            name=name,
        )
        return category

    def _make_recipe(
            self,
            title='test_title',
            description='test_description',
            slug='test-slug-1',
            preparation_time=1,
            servings=1,
            preparation_steps='test_preparation_steps',
            preparation_steps_is_html=False,
            is_published=True,
            category_data=None,
            author_data=None,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        recipe = Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            servings=servings,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=self._make_test_image(),
            category=self._make_category(**category_data),
            author=self._make_author(**author_data)
        )
        return recipe

    def _make_recipe_at_scale(
            self,
            qtd
    ):
        recipes = []
        for i in range(qtd):
            title = f'test_title{i}',
            description = f'test_description{i}',
            slug = f'test-slug-1{i}',
            preparation_steps = f'test_preparation_steps{i}',

            recipe = Recipe.objects.create(
                title=title,
                description=description,
                slug=slug,
                preparation_time=1,
                servings=1,
                preparation_steps=preparation_steps,
                preparation_steps_is_html=False,
                is_published=True,
                cover=self._make_test_image(),
                category=self._make_category(name='test_category'),
                author=self._make_author(
                    first_name=f'f_name{i}',
                    last_name=f'l_name{i}',
                    username=f'username{i}',
                )
            )
            recipes.append(recipe)
        return recipes
