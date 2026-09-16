from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeHomeListView.as_view(), name='recipe_list'),
    path('recipes/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/search/', views.RecipeSearchListView.as_view(), name='recipe_search'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/update/<int:pk>/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/category/<int:cat_pk>/', views.RecipeCategoryListView.as_view(), name='category_list'),
]
