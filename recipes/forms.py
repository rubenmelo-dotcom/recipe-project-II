from django import forms
from recipes.models import Recipe, Category
from django.forms import ModelForm, ValidationError
from django import forms
from collections import defaultdict
from utils.strings import is_positive_number


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'cover': forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        self._my_errors = defaultdict(list)

        omit_field_prep_steps_is_html = kwargs.pop('omit_field_prep_steps_is_html', False)
        omit_field_is_published = kwargs.pop('omit_field_is_published', False)
        omit_field_author = kwargs.pop('omit_field_author', False)
        super().__init__(*args, **kwargs)
        if omit_field_prep_steps_is_html:
            del self.fields['preparation_steps_is_html']
        if omit_field_is_published:
            del self.fields['is_published']
        if omit_field_author:
            del self.fields['author']

    def clean(self):
        super_clean = super().clean()
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append('The title cannot be the same as the description.')
            self._my_errors['description'].append('The description cannot be the same as the title.')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('The title must be at least 5 characters long.')

        return title

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append('Must be a positive number')

        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if not is_positive_number(servings):
            self._my_errors['servings'].append('Must be a positive number')

        return servings
