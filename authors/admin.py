from django.contrib import admin
from authors.models import Profile


@admin.register(Profile)
class ProfilleAdmin(admin.ModelAdmin):
    list_display = 'pk', 'author',
    search_fields = 'pk', 'author',
    list_per_page = 10
