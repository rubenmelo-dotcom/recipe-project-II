from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home_list_view, name='recipe_list'),
    path('recipes/category/<int:cat_pk>/', views.category_list_view, name='category_list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
]
