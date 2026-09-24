from django.urls import path
from authors import views
from django.contrib.auth.decorators import login_required

app_name = 'authors'

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='author_profile'),
    path('register/', views.AuthorRegisterView.as_view(), name='author_register'),
    path('login/', views.AuthorLoginView.as_view(), name='author_login'),
    path('logout/', login_required(views.LogoutView.as_view()), name='author_logout'),
    path('dashboard/', views.AuthorDashboardView.as_view(), name='author_dashboard'),
]
