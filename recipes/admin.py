from django.contrib import admin
from recipes.models import Recipe, Category
from tag.models import Tag
from django.contrib.contenttypes.admin import GenericStackedInline


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published', 'category', 'author',
    ordering = '-id',
    list_editable = 'is_published',
    list_per_page = 10
    list_filter = 'category', 'author', 'is_published',
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = 'title', 'description', 'preparation_steps',
    autocomplete_fields = 'tags',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    ordering = '-id',
    list_per_page = 10
    list_filter = 'name',
