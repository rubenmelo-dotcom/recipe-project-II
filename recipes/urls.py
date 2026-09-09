from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home_list_view, name='recipe_list'),
    path('recipes/delete/', views.recipe_delete_view, name='recipe_delete'),
    path('recipes/create/', views.recipe_create_view, name='recipe_create'),
    path('recipes/search/', views.recipe_search_view, name='recipe_search'),
    path('recipes/<int:pk>/', views.recipe_detail_view, name='recipe_detail'),
    path('recipes/update/<int:pk>/', views.recipe_update_view, name='recipe_update'),
    path('recipes/category/<int:cat_pk>/', views.category_list_view, name='category_list'),
]
