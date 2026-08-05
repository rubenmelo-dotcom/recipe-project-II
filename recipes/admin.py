from django.contrib import admin
from recipes.models import Recipe, Category


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published', 'category', 'author',
    ordering = '-id',
    list_editable = 'is_published',
    list_per_page = 10
    list_filter = 'title', 'category', 'author',
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    ordering = '-id',
    list_per_page = 10
    list_filter = 'name',
