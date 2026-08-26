from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_test, name='author_register'),
    path('login/', views.login_test, name='author_login'),
    path('logout/', views.logout_test, name='author_logout'),
]
