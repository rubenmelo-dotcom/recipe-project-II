from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.test_view, name='home'),
]
