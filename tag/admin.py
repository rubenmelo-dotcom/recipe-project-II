from django.contrib import admin
from tag.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'slug',
    prepopulated_fields = {
        'slug': ('name',)
    }
    search_fields = 'pk', 'name', 'slug',
    list_per_page = 10
    ordering = '-pk',
